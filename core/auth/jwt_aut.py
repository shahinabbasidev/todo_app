from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from users.models import UserModel
from sqlalchemy.orm import Session
from core.database import get_db
from datetime import datetime,timedelta
import jwt
from jwt.exceptions import InvalidSignatureError,DecodeError,ExpiredSignatureError
from core.config import settings

security = HTTPBearer(auto_error=False)

def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID missing in token")

        if decoded.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

        user_obj = db.query(UserModel).filter_by(id=user_id).first()
        if not user_obj:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user_obj

    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Authentication failed {e}")


def generate_access_token(user_id:int ,expires_in:int = 60*5) ->str:

    now = datetime.utcnow()
    payload = {
    "type": "access",
    "user_id": user_id,
    "iat": int(now.timestamp()),
    "exp": int((now + timedelta(seconds=expires_in)).timestamp())
}
    return jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm="HS256")

def generate_refresh_token(user_id:int ,expires_in:int = 3600*24) ->str:

    now = datetime.utcnow()
    payload = {
    "type": "refresh",
    "user_id": user_id,
    "iat": int(now.timestamp()),
    "exp": int((now + timedelta(seconds=expires_in)).timestamp())
}
    return jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm="HS256")

def decode_refresh_token(token):

    try:
        decoded =jwt.decode(token, settings.JWT_SECRET_KEY, algorithms="HS256")
        user_id = decoded.get("user_id",None)
        if not user_id:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail="Authenticate failed, user_id not in the payload")
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authenticate failed, invalid token")
        
        return user_id

    except InvalidSignatureError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail= "Authenticate failed , invalid signature")
    except DecodeError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail="Invalid token format")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token has expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= f"Authenticate failed {e}")
    
access = generate_access_token(1)
refresh = generate_refresh_token(1)
token = generate_access_token(1)
print(token)

