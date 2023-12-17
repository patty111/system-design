from config import config
from fastapi import APIRouter, Request, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from auth.auth import check_valid_credential, create_access_token, get_login_user
from dbHelper import get_db
from sqlmodel import select, Session, col
from models.user import User
from schemas.user_schema import UserRegister, UserInfo
from schemas.token_schema import Token
import secrets
from datetime import datetime, timedelta
from passlib.context import CryptContext

router = APIRouter(tags=["user"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", 
            status_code=status.HTTP_201_CREATED,
            response_model=UserInfo,
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
        password_hash=pwd_context.hash((user.password + salt))
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user.toUserInfo()

@router.post("/token",
            status_code=status.HTTP_201_CREATED,
            response_model=Token,
            summary="Login to get token",
            description="Login to get token",
            responses={
                status.HTTP_201_CREATED: {"description": "login success"},
                status.HTTP_401_UNAUTHORIZED: {"description": "login failed"},
                status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "invalid input or missing fields"}
            })
async def login_and_get_token(request: Request, login_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    stmt = select(User).where(col(User.username) == login_form.username)
    user = db.exec(stmt).one_or_none()

    if not check_valid_credential(login_form, db):
        raise HTTPException(status_code=401, detail="incorrect username or password")

    token: Token = create_access_token(
        data={"user": user.username,
              "exp": datetime.utcnow() + timedelta(int(config.access_token_expire_minutes))
        }
    )
    
    user.last_login = datetime.now()
    db.commit()
    db.refresh(user)

    return token

@router.get("/users/me",
            status_code=status.HTTP_200_OK,
            response_model=UserInfo,
            summary="Get user info",
            description="Get user info",
            responses={
                status.HTTP_200_OK: {"description": "user info"},
                status.HTTP_404_NOT_FOUND: {"description": "user not found"}
            })
async def get_user_info(request: Request, user_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_login_user(db, user_token)
    return user