from fastapi import Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.sql.functions import current_user
import httpx
from app import schemas, models,  oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import datetime
from sqlalchemy import Date
from fastapi import FastAPI, Response, status,HTTPException
from sqlalchemy.orm import Session
from app import models
from passlib.context import CryptContext
import secrets
import os

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
IP_URL = os.environ.get("IP_URL")
WEATHER_API_URL = os.environ.get("WEATHER_API_URL")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


#utility functions for user logins(admin and regular)
def hash_password(user_password: str):

    return pwd_context.hash(user_password)

def compare_password(hashed_password: str, user_password: str):
    return pwd_context.verify(user_password, hashed_password)




def login(db:Session, username:str, password:str, is_admin:bool):
    user_db = None
    if is_admin:
        user_db = db.query(models.AdminUser).filter(models.AdminUser.user_email_admin == username).first()
    if not is_admin:
        user_db = db.query(models.User).filter(models.User.user_email == username).first()
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not compare_password(user_db.user_password, password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = oauth2.create_jwt_access_token(data={"user_id": user_db.user_id,"is_admin": user_db.is_admin})
    print(access_token)
    return {"access_token": access_token,
            "token_type": "bearer"}


#utility functions for account creation and updates
def update_pass_by_user_id(db:Session, id:int, update_data: dict):
    user_query = db.query(models.User).filter(models.User.user_id == id)
    user_db = user_query.first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="Requested user was not found")

    user_query.update(update_data, synchronize_session=False)
    db.commit()
    return {"Data: success"}


#utility functions for weather and location
async def get_weather_by_ip(lon: float, lat: float) -> dict:
    async with httpx.AsyncClient() as client:

        api_key = WEATHER_API_KEY
        weather_api_url = f"{WEATHER_API_URL}key={api_key}&q={lat},{lon}"
        weather_resp = await client.get(weather_api_url)
        weather_data = weather_resp.json()

        return {
            "weather_data": weather_data
        }




