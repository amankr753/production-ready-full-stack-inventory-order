from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.auth import Token, UserCreate


def register_user(db: Session, payload: UserCreate) -> User:
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")
    user = User(
        full_name=payload.full_name,
        email=str(payload.email).lower(),
        hashed_password=get_password_hash(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")
    return user


def issue_tokens(user: User) -> Token:
    settings = get_settings()
    return Token(
        access_token=create_token(user.email, timedelta(minutes=settings.access_token_expire_minutes), "access"),
        refresh_token=create_token(user.email, timedelta(minutes=settings.refresh_token_expire_minutes), "refresh"),
    )
