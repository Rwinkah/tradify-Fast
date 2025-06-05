from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, Optional
from uuid import uuid4, UUID
from ..schema.transaction import TransactionType
from datetime import datetime

if TYPE_CHECKING:
    from ...wallet.models import Wallet

class Transaction(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    amount: float = Field(default=0)
    wallet_id:UUID = Field(foreign_key='wallet.id')
    tx_type: TransactionType
    currency_code: str 
    swap_currency: str | None
    timestamp: datetime = Field(default_factory=datetime.now)
    wallet: Optional["Wallet"] = Relationship(back_populates="transactions")
    


