from fastapi import APIRouter
from uuid import UUID
from sqlmodel import Session, select
from .models import Wallet
from ..currency.services import CurrencyService
from ..user.models.user import User



class WalletService:
    def __init__(self, session: Session):
       self.session = session

    def get_all_wallets(self)-> list[Wallet]:
        statement = select(Wallet)
        results = self.session.exec(statement)
        return list(results.all())

    def get_wallet(self, user_id: UUID) -> Wallet | None:
        statement = select(User).where(User.id == user_id)
        user_result = self.session.exec(statement)
        user = user_result.first()
        if not user or not user.wallet_id:
            return None
        wallet = self.session.get(Wallet, user.wallet_id)
        return wallet

