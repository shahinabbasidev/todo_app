from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from users.models import UserModel
from sqlalchemy.orm import Session
from core.database import get_db


security = HTTPBasic()


def get_authenticated_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    user_obj = (
        db.query(UserModel)
        .filter(UserModel.username == credentials.username)
        .one_or_none()
    )

    if not user_obj.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user_obj