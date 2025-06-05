from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from .balance import Balance
    from ...transaction.models import Transaction
    from ...user.models import User






class Wallet(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)   
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    last_updated: datetime = Field(default_factory=datetime.now, nullable=False)
    balances: list["Balance"] = Relationship(back_populates="wallet") 
    user: 'User' = Relationship(back_populates='wallet')
    transactions: list['Transaction'] = Relationship(back_populates='wallet')



