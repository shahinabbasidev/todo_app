from fastapi import APIRouter,Depends,HTTPException,Query,status
from fastapi.responses import JSONResponse
from users.models import UserModel
from users.schemas import UserLoginSchema,UserRegisterSchema
from sqlalchemy.orm import Session
from core.database import get_db



router = APIRouter(tags=["users"],prefix="/login")


@router.post("/login")
async def login_user(request:UserLoginSchema,db:Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=request.username.lower()).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user dosent exist")
    if not user_obj.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="password is invalid")

    return {}

@router.post("/register")
async def register_user(request:UserRegisterSchema,db:Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=request.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="user is already exist")
    user_obj = UserModel(username = request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()

    return JSONResponse(content="User registered successfully")