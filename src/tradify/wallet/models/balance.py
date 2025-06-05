from sqlmodel import SQLModel, Field, Relationship
from typing import  TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from datetime import datetime

from ...currency.models import Currency

if TYPE_CHECKING:
    from ...wallet.models import Wallet


class Balance(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    wallet_id: UUID = Field(foreign_key="wallet.id", nullable=False)
    currency_id: UUID = Field(foreign_key='currency.id')
    currency: Optional["Currency"] = Relationship()
    amount: float = Field(default=0.0, nullable=False)
    last_updated: datetime = Field(default_factory=datetime.now, nullable=False)
    wallet: "Wallet" = Relationship(back_populates="balances")


