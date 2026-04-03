from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    user_id: int
    consumed_credits: int
    available_credits: int

    class Config:
        from_attributes = True

class UserDisplay(UserBase):
    user_id: int
    sso_provider: Optional[str] = None
    
    class Config:
        from_attributes = True
