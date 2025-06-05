from sqlmodel import Session, select
import json
import os
from tradify.currency.models.currency import Currency
from tradify.wallet.models.wallet import Wallet
from tradify.wallet.models.balance import Balance
from tradify.user.models.user import User
from tradify.transaction.models import Transaction


def seed_currencies(session: Session):
    json_path = os.path.join(os.path.dirname(__file__), "currencies.json")

    with open(json_path, 'r') as f:
        currencies_data: list[dict] = json.load(f)  # list of dicts, not Currency

    existing_currencies = session.exec(select(Currency)).all()

    currency_codes = [item.code for item in existing_currencies]


    for currency in currencies_data:
        code = currency["code"]
        name = currency.get("name")
        if not code or not name:
            continue
        new_currency = Currency(code=code, name=name)
        if new_currency.code not in currency_codes:
            session.add(new_currency)

    session.commit()
