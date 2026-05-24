from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: EmailStr
    hashed_password: str
    role: str = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class UserInDB(User):
    pass


class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        populate_by_name = True
