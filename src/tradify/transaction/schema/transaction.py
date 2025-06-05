from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class TransactionType(str, Enum):
    FUND = "fund"
    WITHDRAW = "withdraw"
    TRADE = "trade"






class TransactionFund(BaseModel):
    user_id: UUID
    amount: float



class TransactionTrade(BaseModel):
    user_id: UUID
    from_code: str
    to_code: str
    amount: float



class TransactionWithdraw(BaseModel):
    user_id: UUID
    currency_code: str
    amount: float

    
