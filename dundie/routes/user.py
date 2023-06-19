from typing import List

from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from dundie.models.user import User, UserRequest, UserResponse

from dundie.db import ActiveSession
from dundie.auth import AuthenticatedUser, SuperUser
from sqlalchemy.exc import IntegrityError


router = APIRouter()


@router.get("/", response_model=List[UserResponse], dependencies=[AuthenticatedUser])
async def list_users(*, session: Session = ActiveSession):
    """List all users."""
    users = session.exec(select(User)).all()
    return users


@router.get("/{username}/", response_model=UserResponse)
async def get_user_by_username(
    *, session: Session = ActiveSession, username: str
):
    """Get user by username"""
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201, dependencies=[SuperUser])
async def create_user(*, session: Session = ActiveSession, user: UserRequest):
    """Creates new user"""
    # LBYL
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=409, detail="User email already exists.")
    
    db_user = User.from_orm(user)  # transform UserRequest in User
    session.add(db_user)
    # EAFP
    try:
        session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=500,
            detail="Database IntegrityError"
        )
    session.refresh(db_user)
    return db_user