from fastapi import Depends, HTTPException 
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from passlib.context import CryptContext

from jose import jwt, JWTError

from datetime import datetime, timedelta
from app.core.config import settings
from app.db.session import get_db
from app.db.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(subject: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(subject), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
    ):
    try:
        t = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = user_id = int(t.get("sub"))
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
async def get_current_confirmed_user(current_user=Depends(get_current_user)):
    if not current_user.is_confirmed:
        raise HTTPException(status_code=403, detail="Account pending confirmation.")
    return current_user


async def get_current_admin(current_user=Depends(get_current_confirmed_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required.")
    return current_user