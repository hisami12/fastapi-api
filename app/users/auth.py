from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from app.config import get_auth_data
from jose import jwt
from app.users.dao import UserDao
from app.users.dependencies import get_token
from fastapi import Request, HTTPException, Depends, status
# from fastapi.app.config import config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str)->str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)    


def create_access_token(data: dict)-> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt 

async def authenticate_user(user_data):
    user = await UserDao.find_one_or_none(email=user_data.email)
    if not user or verify_password(plain_password=user_data.password, hashed_password=user.password) is False:
        return None
    return user


async def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    return token


async def get_current_user(token = Depends(get_token)):
    auth_data = get_auth_data()
    user_data = jwt.decode(token, auth_data["secret_key"], auth_data["algorithm"])
    user = await UserDao.find_one_or_none(id = int(user_data["sub"]))
    
    
    expire = user_data.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = user_data.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user
