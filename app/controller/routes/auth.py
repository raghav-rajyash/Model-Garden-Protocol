from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.model.user import User
from app.utils.security import verify_password, create_access_token
from app.config.config import settings
import httpx
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.view.user import UserDisplay
from app.view.auth import LoginRequest, Token
from app.utils.seed_data import seed_for_test_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    user = await User.verify_auth_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

router = APIRouter(tags=["auth"])

@router.get("/me", response_model=UserDisplay)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}

@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    user = await User.get_by_username(db, login_data.username)
    if not user or not user.hashed_password or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.username)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{provider}/login")
async def sso_login(provider: str):
    if provider == "google":
        url = (
            f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.google_client_id}"
            f"&redirect_uri={settings.google_redirect_uri}&scope=openid%20profile%20email&access_type=offline"
        )
        return RedirectResponse(url)
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

@router.get("/{provider}/callback")
async def sso_callback(
    provider: str, 
    code: str, 
    db: AsyncSession = Depends(get_db)
):
    if provider != "google":
        raise HTTPException(status_code=400, detail="Unsupported provider")
    
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code",
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid Google code")
        tokens = response.json()
        
        user_info_response = await client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        user_info = user_info_response.json()
        
    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Google email not found")

    user = await User.find_or_create_sso_user(
        session=db,
        email=email,
        sso_provider="google",
        sso_id=str(user_info.get("id") or user_info.get("sub")),
        first_name=user_info.get("given_name", ""),
        last_name=user_info.get("family_name", "")
    )

    if email == "testvariable002@gmail.com":
        await seed_for_test_user(db, user)

    access_token = create_access_token(subject=user.username)
    # Redirect to frontend with token
    frontend_url = f"{settings.frontend_url}/auth/callback?token={access_token}"
    return RedirectResponse(frontend_url)
