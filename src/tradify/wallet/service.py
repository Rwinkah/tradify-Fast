from uuid import UUID
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, select
from .models import Wallet
from ..user.models.user import User
from .models import Balance



class WalletService:
    def __init__(self, session_factory: sessionmaker[Session]):
       self.session_factory = session_factory

    def get_all_wallets(self)-> list[Wallet]:
        with self.session_factory() as session:
            statement = select(Wallet)
            results = session.exec(statement)
            return list(results.all())

    def get_wallet(self, user_id: UUID) -> dict:
        with self.session_factory() as session:
            statement = select(User).where(User.id == user_id)
            user_result =session.exec(statement)
            user = user_result.first()
            if not user or not user.wallet_id:
                return {'success': False, 'code': 'W-GW01'}
            wallet = session.exec(select(Wallet).where(Wallet.id == user.wallet_id)).first()
            if not wallet:
                return {'success': False, 'code': 'W-GW02'}  
            

            balances = session.exec(select(Balance).where(Balance.wallet_id== wallet.id)).all()

            ret_wallet = {**wallet.model_dump(), 'balances': balances}
            return {'success': True, 'read_wallet': ret_wallet, 'wallet': wallet}

