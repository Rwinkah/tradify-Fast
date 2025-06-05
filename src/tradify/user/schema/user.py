from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    firstName: str
    lastName: str
    phoneNumber: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    phoneNumber: str
    password: str  
    
class UserUpdate(BaseModel):
    id: Optional[UUID]
    email: Optional[EmailStr]
    firstName: Optional[str]
    lastName: Optional[str]
    phoneNumber: Optional[str]
    is_active: Optional[bool]
    is_verified: Optional[bool]



class UserDelete(BaseModel):
    id: UUID