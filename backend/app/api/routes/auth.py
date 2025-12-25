"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserRegister, UserResponse, Token
from app.services.auth_service import AuthService
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    """
    Register a new user account.
    
    - **email**: Valid email address (must be unique)
    - **username**: Username (3-100 characters, must be unique)
    - **password**: Password (minimum 8 characters)
    """
    service = AuthService(db)
    
    try:
        result = service.register_user(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
        )
        return Token(
            access_token=result["access_token"],
            token_type=result["token_type"],
            user=UserResponse(**result["user"])
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.post("/login", response_model=Token)
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Login with username and password.
    
    Returns an access token for authenticated requests.
    Uses form data (application/x-www-form-urlencoded) for OAuth2 compatibility.
    """
    service = AuthService(db)
    
    try:
        result = service.login_user(
            username=username,
            password=password,
        )
        return Token(
            access_token=result["access_token"],
            token_type=result["token_type"],
            user=UserResponse(**result["user"])
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    Get current authenticated user information.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat(),
    )

