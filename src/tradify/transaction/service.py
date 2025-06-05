from sqlmodel import  select, Session
from sqlalchemy.orm import sessionmaker
from uuid import UUID
from ..currency.services import CurrencyService
from ..wallet.service import WalletService
from tradify.wallet.models import Balance, Wallet
import time
from .models import Transaction
from .schema import TransactionType
from tradify.user.service import UserService
from tradify.user.models import User

class TransactionService:
    def __init__(self, session_factory:sessionmaker[Session]):  # Accept a session factory (e.g. sessionmaker)
        self.session_factory = session_factory
        self.wallet_service = WalletService(session_factory)
    def fund(self, user_id: UUID, amount: float):
        with self.session_factory() as session:
            currency_service = CurrencyService(session)

            result = self.wallet_service.get_wallet(user_id)
            
            if not isinstance(result,dict):
                return {"success": False, "code":'T-F01'}   
            wallet = result.get('wallet')
            if not isinstance(wallet, Wallet):
                return {"success": False, "code":'T-F01'}

            currency = currency_service.currency_get_default()
            if not currency:
                return {"success": False, "code":'T-F02'}
          


            for attempt in range(4):    
                try:
                    balance = next((b for b in wallet.balances if b.currency_id == currency.id), None)

                    if not balance:
                        balance = Balance(wallet_id=wallet.id, currency_id=currency.id, amount=0.0)
                        session.add(balance)
                        session.commit()
                        session.refresh(balance)

                    if not balance:
                        return {"success": False, "code":'T-F03'}

                    current = session.exec(
                        select(Balance)
                        .where(Balance.id == balance.id)
                        .with_for_update()
                    ).first()

                    if not current:
                        time.sleep(0.05)
                        continue

                    current.amount += amount
                    session.add(current)
                    session.commit()
                    session.refresh(current)

   
                    self.create_record(
                        session=session,
                        wallet_id=wallet.id,
                        tx_type=TransactionType('fund'),
                        amount=amount,
                        from_code=currency.code,
                        to_code=None
                    )
                    return {"success": True, "code":'T-F00'}
    

                except Exception as e:
                    print('-----------------------------------------------')
                    print(e)
                    print('-----------------------------------------------')
                    session.rollback()
                    time.sleep(0.05)
                    continue 

            return {"success": False, "code":'T-F04'}

    def withdraw(self, user_id: UUID, currency_code: str, amount: float):
        with self.session_factory() as session:
            currency_service = CurrencyService(session)

            result = self.wallet_service.get_wallet(user_id)
            if not isinstance(result,dict):
                return {"success": False, "code":'T-W01'}   
            wallet = result.get('wallet')
            if not isinstance(wallet, Wallet):
                return {"success": False, "code":'T-W01'}

            currency = currency_service.currency_get(currency_code)
            if not currency:
                return {'success': False, 'code': 'T-W02'}

            balance = next((b for b in wallet.balances if b.currency_id == currency.id), None)
            if not balance:
                return {'success': False, 'code': 'T-W03'}

            for attempt in range(4):
                try:
                    current = session.exec(
                        select(Balance)
                        .where(Balance.id == balance.id)
                        .with_for_update()
                    ).first()

                    if not current:
                        session.rollback()
                        time.sleep(0.05)
                        continue

                    if current.amount < amount:
                        session.rollback()
                        return {'success': False, 'code': 'T-W04'}

                    current.amount -= amount
                    session.add(current)
                    session.commit()
                    session.refresh(current)
                    self.create_record(session=session, wallet_id=wallet.id, tx_type=TransactionType('withdraw'), amount=amount, from_code=currency.code, to_code=None)
                    return {'success': True, 'code': 'T-W00'}

                except Exception:
                    session.rollback()
                    time.sleep(0.05)
                    continue

            return {'success': False, 'code': 'T-W05'}

    def trade(self, user_id: UUID, from_code: str, to_code: str, amount: float):
        with self.session_factory() as session:
            currency_service = CurrencyService(session)

            result = self.wallet_service.get_wallet(user_id)

            if not isinstance(result,dict):
                return {"success": False, "code":'T-S01'}   
            wallet = result.get('wallet')
            if not isinstance(wallet, Wallet):
                return {"success": False, "code":'T-S01'}


            from_currency = currency_service.currency_get(from_code)
            to_currency = currency_service.currency_get(to_code)
            if not from_currency or not to_currency:
                return {'success': False, 'code': 'T-S02'}

            from_balance = next((b for b in wallet.balances if b.currency_id == from_currency.id), None)
            to_balance = next((b for b in wallet.balances if b.currency_id == to_currency.id), None)

            if not from_balance or from_balance.amount < amount:
                return {'success': False, 'code': 'T-S03'}

            if not to_balance:
                to_balance = Balance(wallet_id=wallet.id, currency_id=to_currency.id, amount=0.0)
                session.add(to_balance)
                session.commit()
                session.refresh(to_balance)

            for attempt in range(4):
                try:
                    from_current = session.exec(
                        select(Balance)
                        .where(Balance.id == from_balance.id)
                        .with_for_update()
                    ).first()
                    to_current = session.exec(
                        select(Balance)
                        .where(Balance.id == to_balance.id)
                        .with_for_update()
                    ).first()

                    if not from_current or not to_current:
                        session.rollback()
                        time.sleep(0.05)
                        continue

                    if from_current.amount < amount:
                        session.rollback()
                        return {'success': False, 'code': 'T-S04'}

                    # For simplicity, 1:1 swap rate
                    from_current.amount -= amount
                    to_current.amount += amount

                    session.add(from_current)
                    session.add(to_current)
                    session.commit()
                    session.refresh(from_current)
                    session.refresh(to_current)
                    self.create_record(session=session, wallet_id=wallet.id, tx_type=TransactionType('trade'), amount=amount, from_code=from_currency.code, to_code=to_currency.code)

                    return {'success': True, 'code': 'T-S00'}

                except Exception as e:
                    print(e)
                    session.rollback()
                    time.sleep(0.05)
                    continue

            return {'success': False, 'code': 'T-S05'}

    def create_record(self, session: Session, wallet_id:UUID, tx_type: TransactionType, amount: float, to_code:str|None, from_code:str):
        tx = Transaction(
            tx_type=tx_type,
            amount=amount,
            currency_code= from_code,
            swap_currency=to_code,
            wallet_id=wallet_id
        )


        session.add(tx)
        session.commit()
        session.refresh(tx)
        return tx

    def get_all_transactions(self) -> list[Transaction]:
        with self.session_factory() as session:
            statement = select(Transaction)
            transactions = session.exec(statement).all()
            return list(transactions)
    def get_all_user_transactions(self, user_id:UUID)-> list[Transaction]:
        with self.session_factory() as session:
            user = session.exec(select(User).where(User.id == user_id)).first()
            if not user:
                return []
            
            statement = select(Transaction).where(Transaction.wallet_id == user.wallet_id)
            transactions = session.exec(statement).all()
            return list(transactions)

