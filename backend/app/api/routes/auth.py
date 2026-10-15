"""Authentication and user management API endpoints"""
from typing import Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models import User, UserProfile
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


# Pydantic schemas
class RegisterRequest(BaseModel):
    """Request schema for user registration"""
    open_id: str = Field(..., description="Unique open ID (e.g. WeChat open_id)")
    name: Optional[str] = Field(None, description="Display name")
    phone: Optional[str] = Field(None, description="Phone number")


class LoginRequest(BaseModel):
    """Request schema for user login"""
    open_id: str = Field(..., description="User open ID")


class TokenResponse(BaseModel):
    """Response schema for authentication tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    """Request schema for token refresh"""
    refresh_token: str = Field(..., description="Refresh token")


class UserProfileResponse(BaseModel):
    """Response schema for user profile"""
    user_id: UUID
    open_id: str
    name: Optional[str]
    avatar_url: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProfileDetailResponse(BaseModel):
    """Response schema for detailed user profile"""
    profile_id: UUID
    user_id: UUID
    bio: Optional[str]
    expertise_levels: Optional[dict]
    learning_preferences: Optional[dict]
    maslow_scores: Optional[dict]
    mask_scores: Optional[dict]
    seven_habits_scores: Optional[dict]
    current_level: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    """Request schema for updating user profile"""
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    expertise_levels: Optional[dict] = None
    learning_preferences: Optional[dict] = None
    maslow_scores: Optional[dict] = None
    mask_scores: Optional[dict] = None
    seven_habits_scores: Optional[dict] = None
    current_level: Optional[str] = None


@router.post("/register", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new user account.

    Creates a User record and an associated UserProfile with default scores.
    Returns the newly created user profile.
    """
    existing = db.query(User).filter(User.open_id == request.open_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this open_id already exists")

    user = User(
        open_id=request.open_id,
        name=request.name,
        phone=request.phone,
    )
    db.add(user)
    db.flush()  # populate user.user_id

    profile = UserProfile(user_id=user.user_id)
    db.add(profile)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT access + refresh tokens.

    The open_id is used as the credential.  If the user does not exist a
    401 error is returned.
    """
    user = db.query(User).filter(User.open_id == request.open_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is disabled")

    user_id_str = str(user.user_id)
    return TokenResponse(
        access_token=create_access_token(user_id_str),
        refresh_token=create_refresh_token(user_id_str),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db),
):
    """
    Exchange a valid refresh token for a new access + refresh token pair.
    """
    try:
        payload = verify_token(request.refresh_token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token is not a refresh token")

    user_id_str = payload.get("sub")
    user = db.query(User).filter(User.user_id == UUID(user_id_str)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or disabled")

    return TokenResponse(
        access_token=create_access_token(user_id_str),
        refresh_token=create_refresh_token(user_id_str),
    )


@router.get("/me", response_model=dict)
async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Get the current authenticated user's profile.

    Returns both the User record and the associated UserProfile with
    MASK / Maslow / expertise scores.
    """
    user_uuid = UUID(user_id)

    user = db.query(User).filter(User.user_id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.query(UserProfile).filter(UserProfile.user_id == user_uuid).first()

    return {
        "user": {
            "user_id": str(user.user_id),
            "open_id": user.open_id,
            "name": user.name,
            "avatar_url": user.avatar_url,
            "email": user.email,
            "phone": user.phone,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        },
        "profile": {
            "profile_id": str(profile.profile_id) if profile else None,
            "bio": profile.bio if profile else None,
            "expertise_levels": profile.expertise_levels if profile else {},
            "learning_preferences": profile.learning_preferences if profile else {},
            "maslow_scores": profile.maslow_scores if profile else {},
            "mask_scores": profile.mask_scores if profile else {},
            "seven_habits_scores": profile.seven_habits_scores if profile else {},
            "current_level": profile.current_level if profile else "beginner",
        },
    }


@router.put("/me", response_model=dict)
async def update_user_profile(
    request: UpdateProfileRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Update the current authenticated user's profile.

    Accepts partial updates -- only provided fields are changed.
    """
    user_uuid = UUID(user_id)

    user = db.query(User).filter(User.user_id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update User fields
    if request.name is not None:
        user.name = request.name
    if request.avatar_url is not None:
        user.avatar_url = request.avatar_url
    if request.email is not None:
        user.email = request.email
    if request.phone is not None:
        user.phone = request.phone

    # Update UserProfile fields
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_uuid).first()
    if not profile:
        profile = UserProfile(user_id=user_uuid)
        db.add(profile)

    if request.bio is not None:
        profile.bio = request.bio
    if request.expertise_levels is not None:
        profile.expertise_levels = request.expertise_levels
    if request.learning_preferences is not None:
        profile.learning_preferences = request.learning_preferences
    if request.maslow_scores is not None:
        profile.maslow_scores = request.maslow_scores
    if request.mask_scores is not None:
        profile.mask_scores = request.mask_scores
    if request.seven_habits_scores is not None:
        profile.seven_habits_scores = request.seven_habits_scores
    if request.current_level is not None:
        profile.current_level = request.current_level

    db.commit()
    db.refresh(user)
    db.refresh(profile)

    return {
        "user_id": str(user.user_id),
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "bio": profile.bio,
        "expertise_levels": profile.expertise_levels,
        "mask_scores": profile.mask_scores,
        "maslow_scores": profile.maslow_scores,
        "current_level": profile.current_level,
        "message": "Profile updated successfully",
    }
