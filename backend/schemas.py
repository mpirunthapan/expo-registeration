from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class RegistrationBase(BaseModel):
    fullname: str
    email: EmailStr
    phone_number: str
    age: int
    work_station: Optional[str] = None
    category: str
    heard_from: str
    joined_community: bool = False

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationOut(RegistrationBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class AdminUserBase(BaseModel):
    email: EmailStr
    is_active: bool = True

class AdminUserCreate(AdminUserBase):
    email: EmailStr
    password: str

class AdminUserOut(AdminUserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class AdminUserLogin(BaseModel):
    email: EmailStr
    password: str

class AdminPasswordUpdate(BaseModel):
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class NewsletterSubscriberBase(BaseModel):
    email: EmailStr

class NewsletterSubscriberCreate(NewsletterSubscriberBase):
    pass

class NewsletterSubscriberOut(NewsletterSubscriberBase):
    id: int
    is_active: bool
    subscribed_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )