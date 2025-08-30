from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from fastapi import  Form, File, UploadFile


class UserCreate(BaseModel):
    user_email: EmailStr
    user_password: str

class UserCreateResponse(BaseModel):
    user_email: EmailStr

class UserUpdatePassword(BaseModel):
    user_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class AccessTokenData(BaseModel):
    user_id: Optional[int] = None
    is_admin: Optional[bool] = None

class Location(BaseModel):
    lat: float
    lon: float

class PostInfo(BaseModel):
    title: str
    content: str
    category: str

    model_config = {
        "from_attributes": True
    }

class PostResponse(BaseModel):
    title: str
    content: str


    model_config = {
        "from_attributes": True
    }

class PromptRequest(BaseModel):
    prompt: str

class DiseaseImage(BaseModel):
    image: UploadFile = File(...)

    model_config = {
        "from_attributes": True
    }