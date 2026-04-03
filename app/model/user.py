from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.config.config import settings


class User(SQLModel, table=True):
    __tablename__ = "user"

    user_id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(unique=True, index=True)
    hashed_password: Optional[str] = None
    first_name: str
    last_name: str
    email: str = Field(unique=True, index=True)
    phone_number: Optional[str] = None
    photograph: Optional[bytes] = None

    consumed_credits: int = 0
    available_credits: int = 0
    
    sso_provider: Optional[str] = None
    sso_id: Optional[str] = None

    # RELATIONSHIPS
    owned_workspaces: List["Workspace"] = Relationship(back_populates="owner")
    project_memberships: List["ProjectMember"] = Relationship(back_populates="user")
    
    @staticmethod
    async def get_by_username(session: AsyncSession, username: str) -> Optional["User"]:
        from sqlmodel import select
        statement = select(User).where(User.username == username)
        result = await session.execute(statement)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> Optional["User"]:
        from sqlmodel import select
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def find_or_create_sso_user(
        session: AsyncSession, 
        email: str, 
        sso_provider: str, 
        sso_id: str,
        first_name: str = "",
        last_name: str = ""
    ) -> "User":
        user = await User.get_by_email(session, email)
        if not user:
            user = User(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                sso_provider=sso_provider,
                sso_id=sso_id
            )
            session.add(user)
        else:
            # Update existing user if SSO info is missing
            if not user.sso_id:
                user.sso_provider = sso_provider
                user.sso_id = sso_id
                session.add(user)
        
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def verify_auth_token(session: AsyncSession, token: str) -> Optional["User"]:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            if username is None:
                return None
        except JWTError:
            return None
        
        return await User.get_by_username(session, username)
