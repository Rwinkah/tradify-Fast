from sqlmodel import SQLModel, Field, Relationship
from typing import  TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime



from ...wallet.models.wallet import Wallet
# if TYPE_CHECKING:



class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(index=True, unique=True, nullable=False)
    firstName: str = Field(unique=False, nullable=False)
    lastName: str = Field(unique=False, nullable=False)
    phoneNumber: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_verified: bool =Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    wallet_id: UUID = Field(foreign_key='wallet.id', unique=True, nullable=False)
    wallet: "Wallet" = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})





