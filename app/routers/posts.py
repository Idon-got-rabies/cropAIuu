from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from app import schemas, models, functions,database, config, oauth2
from sqlalchemy.orm import Session
import aiofiles, os, uuid
from starlette.concurrency import run_in_threadpool
from fastapi import  Form, File, UploadFile
router = APIRouter(prefix="/posts",
                   tags=["posts"])






@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(skip: int = 0, limit: int = 10,
                     db: Session = Depends(database.get_db)):

    def sync_db():
        posts = db.query(models.Post).offset(skip).limit(limit).all()
        return posts

    return await run_in_threadpool(sync_db)



@router.post("/create/", response_model=schemas.PostResponse)
async def create_post(post_info: schemas.PostInfo,
                      db: Session = Depends(database.get_db),
                      current_user = Depends(oauth2.get_current_user)):

    def sync_db():
        new_post = models.Post(**post_info.model_dump(by_alias=True))
        new_post.user_id = current_user.user_id
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return {
            "title": new_post.title,
            "content": new_post.content,
        }
    return await run_in_threadpool(sync_db)
