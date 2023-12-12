from fastapi import APIRouter, Request, status, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from sqlmodel import select, update, Session, col
from models.url import Url
from dbHelper import get_db
from config import config
from models.user import UserRegister, User
import secrets
import hashlib

router = APIRouter(tags=["user"])

@router.post("/register", 
            status_code=status.HTTP_201_CREATED,
            summary="Register new user",
            description="Register new user",
            responses={
                status.HTTP_201_CREATED: {"description": "user created"},
                status.HTTP_409_CONFLICT: {"description": "username already exists"},
                status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "invalid input or missing fields"}
            })
async def register(request: Request, user: UserRegister, db: Session = Depends(get_db)):
    stmt = select(User).where(col(User.username) == user.username)
    exist_user = db.exec(stmt).one_or_none()

    if exist_user is not None:
        raise HTTPException(status_code=409, detail="username already exists")
    
    salt = secrets.token_bytes(10).hex()
    user = User(
        username=user.username,
        salt=salt,
        password_hash=hashlib.md5((user.password + salt).encode("utf-8")).hexdigest()
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    raise HTTPException(status_code=201, detail="user created")

# TODO: add login check
@router.get("/{username}/info",
            status_code=status.HTTP_200_OK,
            summary="Get user info",
            description="Get user info",
            responses={
                status.HTTP_200_OK: {"description": "user info"},
                status.HTTP_404_NOT_FOUND: {"description": "user not found"}
            })
async def get_user_info(request: Request, username: str, db: Session = Depends(get_db)):
    stmt = select(User).where(col(User.username) == username)
    user = db.exec(stmt).one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    
    raise HTTPException(status_code=200, detail=jsonable_encoder(user))
