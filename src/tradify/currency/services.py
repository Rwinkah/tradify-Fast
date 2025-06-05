from sqlmodel import Session, select
from .models import Currency
import os



class CurrencyService:

    def __init__(self, session:Session):
        self.session =  session
    def currency_get(self, code: str)-> Currency | None:
        statement = select(Currency).where(Currency.code == code)
        currency = self.session.exec(statement).first()
        if not currency:
            return None
        return currency

    def currency_get_default(self)->Currency | None:
        env_currency = os.getenv('DEF_CURRENCY')
        if env_currency:
            def_currency = self.session.exec(select(Currency).where(Currency.code == env_currency.capitalize()))
            if def_currency:
                return def_currency.first()
        statement = select(Currency).where(Currency.code == 'NGN')
        return self.session.exec(statement).first()
         

    