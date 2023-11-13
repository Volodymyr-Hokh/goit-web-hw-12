from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class ContactRequest(BaseModel):
    first_name: str = Field(min_length=2, max_length=20)
    last_name: str = Field(max_length=20)
    email: Optional[EmailStr]
    phone_number: Optional[str] = Field(pattern=r"^\+?[1-9][\d]{11}$")
    birthday: Optional[date]


class ContactResponse(ContactRequest):
    id: int

    class Config:
        from_attributes = True
