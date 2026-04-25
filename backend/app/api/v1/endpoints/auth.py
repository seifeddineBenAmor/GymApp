from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import verify_password, hash_password, create_access_token
from app.db.session import get_db
from app.db.models import User

from app.schemas import RegisterRequest, LoginRequest, UserResponse



router = APIRouter()

@router.post("/register", status_code=201, response_model=UserResponse)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    email = body.email
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=409, detail="Email already registered.")

    pwd_hash = hash_password(body.password)
    user = User(
        email = email,
        password_hash = pwd_hash,
        name = body.name,
        family_name= body.family_name,
        gender= body.gender,
        is_confirmed=False,
        is_admin=False,
        photo="/static/users/no_image.jpg",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login")
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    email=body.email
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="User does not exist or wrong password.")
    if not user.is_confirmed:
        raise HTTPException(status_code=403, detail="User not confirmed yet.")
    
    return {"access_token": create_access_token(user.id), "token_type": "bearer"}

    