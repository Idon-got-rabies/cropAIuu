from fastapi import Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.sql.functions import current_user

from app import schemas, models, functions, oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette.concurrency import run_in_threadpool

router = APIRouter(prefix="/auth",
                   tags=["auth"])

@router.get("/me/")
async def token_check(current_user: models.User = Depends(oauth2.get_current_user)):
    return "valid"


@router.post("/login/")
async def user_login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    def sync_db():
        return functions.login(db,user_cred.username, user_cred.password, is_admin=False)


    return await run_in_threadpool(sync_db)

@router.post("/login/admin/")
async def admin_login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    def sync_db():
        functions.login(db,user_cred.username, user_cred.password, is_admin=True)

    return await run_in_threadpool(sync_db)


