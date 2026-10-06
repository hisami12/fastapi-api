from fastapi import Request, HTTPException, status, Depends
from app.config import get_auth_data
from jose import jwt
from app.users.dao import UserDao
from datetime import datetime, timezone
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



async def get_current_admin_user(current_user = Depends(get_current_user)):
    print(type(current_user.is_admin))
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you do not have premission to perform this action")
    return current_user