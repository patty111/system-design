from dbHelper import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from sqlmodel import select, col, Session
from models.user import User
from schemas.token_schema import Token
from schemas.user_schema import UserInfo
from passlib.context import CryptContext
from datetime import datetime, timedelta
from config import config
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def check_valid_credential(user_input: OAuth2PasswordRequestForm, db = get_db()):
    """
    Authenticate user by username and password
    """

    stmt = select(User).where(col(User.username) == user_input.username)
    user = db.exec(stmt).one_or_none()

    if user is None:
        return False
    
    if not pwd_context.verify((user_input.password + user.salt), user.password_hash):
        return False
    
    return True

def create_access_token(data: dict, expires_delta: timedelta = None) -> Token:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(config.access_token_expire_minutes))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)

    return {"access_token": encoded_jwt, "token_type": "bearer"}

def get_login_user(db: Session, token: str = Depends(oauth2_scheme)) -> UserInfo:
    """
    Get login info user by token
    """
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        username: str = payload.get("user")
        if username is None:
            raise HTTPException(status_code=401, detail="User not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    stmt = select(User).where(col(User.username) == username)
    user = db.exec(stmt).one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user.toUserInfo()