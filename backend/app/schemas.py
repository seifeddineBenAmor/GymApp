from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date, datetime

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name :str
    number_of_instances :int
    icone_path: str
    icone_path_female: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    family_name: str
    gender: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    name: str
    family_name: str
    gender: str
    photo: str
    is_confirmed: bool
    is_admin: bool
    program_id: Optional[int]
    expire_date: Optional[date]
    date_of_birth: Optional[date]
    created_at: datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
