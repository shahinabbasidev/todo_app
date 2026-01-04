from fastapi import APIRouter,Depends,HTTPException,Query,status
from fastapi.responses import JSONResponse
from users.models import UserModel,TokenModel
from users.schemas import UserLoginSchema,UserRegisterSchema,UserRefreshTokenSchema
from sqlalchemy.orm import Session
from core.database import get_db
import secrets
from auth.jwt_aut import generate_access_token,generate_refresh_token,decode_refresh_token



router = APIRouter(tags=["users"],prefix="/login")
def generate_token(length=32):

    return secrets.token_hex(length)


@router.post("/login")
async def login_user(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=request.username.lower()).first()

    if not user_obj or not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)  # ✅ تصحیح شد

    return {
        "detail": "Logged in successfully",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(
        UserModel.username.ilike(request.username)
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )

    user_obj = UserModel(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return {"detail": "User registered successfully", "user_id": user_obj.id}
@router.post("/refresh-token")
async def refresh_token(request: UserRefreshTokenSchema, db: Session = Depends(get_db)):
    try:
        user_id = decode_refresh_token(request.token)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user_obj = db.query(UserModel).filter_by(id=user_id).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    new_access_token = generate_access_token(user_id)
    return {"access_token": new_access_token, "token_type": "bearer"}