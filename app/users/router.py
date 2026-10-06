from fastapi import APIRouter, HTTPException, status, Response, Request, Depends
from app.users.auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from app.users.dao import UserDao
from app.users.schemas import SUuserRegister, SUserAuth
from app.users.dependencies import get_current_user
from app.users.dependencies import get_current_admin_user


router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/register/")
async def register(user_data: SUuserRegister):
    user = await UserDao.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(status_code=409, detail="user already exists")

    user_new_instance = user_data.model_dump()
    user_new_instance["password"] = get_password_hash(user_data.password)
    await UserDao.add(**user_new_instance)
    return {"message": "You have successfuly registered!"}
    


@router.post("/login/")
async def login(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data)
    if not user:
        raise HTTPException(status_code=401, detail="incorrect email or password")
    
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}



@router.get("/me/")
async def me(user = Depends(get_current_user)):
    return user

@router.get("/loggout_user")
async def loggout(response: Response):
    response.delete_cookie(key="user_access_token")
    return{"message": "User successfully deleted"}


@router.get("/all_users")
async def get_all_users(is_admin = Depends(get_current_admin_user)):
    return await UserDao.find_all()