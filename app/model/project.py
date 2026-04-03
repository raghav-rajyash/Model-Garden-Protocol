from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.ext.asyncio import AsyncSession


class Project(SQLModel, table=True):
    __tablename__ = "project"

    project_id: Optional[int] = Field(default=None, primary_key=True)

    project_name: str
    project_status: str = Field(default="Draft") # Draft, Hosted, Under Tuning
    project_start_date: Optional[str] = None
    project_owner_sso: Optional[str] = None
    project_credits: int = 0
    project_icon: Optional[bytes] = None
    project_git_repo_url: Optional[str] = None
    project_category: str = Field(default="my-projects") # my-projects, collab, reviews, trainings

    workspace_id: int = Field(foreign_key="workspace.workspace_id")

    # RELATIONSHIPS
    workspace: Optional["Workspace"] = Relationship(back_populates="projects")
    members: List["ProjectMember"] = Relationship(back_populates="project")

    @staticmethod
    async def get_by_user(session: AsyncSession, user_id: int) -> List["Project"]:
        from sqlmodel import select
        from app.model.workspace import Workspace
        statement = select(Project).join(Workspace).where(Workspace.workspace_owner_id == user_id)
        result = await session.execute(statement)
        return result.scalars().all()
