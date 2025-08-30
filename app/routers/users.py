from app import schemas, models, functions, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import get_current_user
from starlette.concurrency import run_in_threadpool

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserCreateResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    def sync():
        hashed_password = functions.hash_password(user.user_password)


        if hashed_password is None:
            raise HTTPException(status_code=500, detail=" password hashing failed")
        user.user_password = hashed_password

        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    return await run_in_threadpool(sync)

@router.post("/admin/")
async def create_admin_user(user: schemas.UserCreate, db: Session = Depends(get_db),
                            current_user: models.User = Depends(get_current_user)):
    def sync_db():
        if not current_user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")

        hashed_password = functions.hash_password(user.user_password)
        if hashed_password is None:
            raise HTTPException(status_code=500, detail=" password hashing failed")
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    return await run_in_threadpool(sync_db)

@router.put("/password/")
async def update_user_pass(id: int,
                     user_pass:schemas.UserUpdatePassword,
                     db: Session = Depends(get_db)):

    def sync():
        return functions.update_pass_by_user_id(db, id, user_pass.model_dump())
    return await run_in_threadpool(sync)
