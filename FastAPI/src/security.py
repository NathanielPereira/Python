from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from src.config import settings

security = HTTPBearer()


def sign_jwt(user_id: int) -> dict:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return {"access_token": token}


def verify_jwt(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload.get("user_id")
    except JWTError:
        return None


async def login_required(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    token = credentials.credentials
    user_id = verify_jwt(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id

