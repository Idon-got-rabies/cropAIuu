import os
from app import schemas, models, functions, oauth2
from fastapi import APIRouter, Depends, HTTPException, status, Request
import requests
from starlette.concurrency import run_in_threadpool

router = APIRouter(prefix="/weather",
                   tags=["weather"])

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
IP_URL = os.environ.get("IP_URL")
WEATHER_API_URL = os.environ.get("WEATHER_API_URL")


@router.get("/")
async def get_current_weather(latitude: float, longitude: float):
    response = await functions.get_weather_by_ip(longitude, latitude)
    return response



