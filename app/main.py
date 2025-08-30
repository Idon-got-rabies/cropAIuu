from fastapi import FastAPI
from app.routers import weather, users, auth, AI_queries,posts
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.include_router(weather.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)

app.include_router(AI_queries.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
