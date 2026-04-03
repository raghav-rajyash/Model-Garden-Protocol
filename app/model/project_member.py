from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class ProjectMember(SQLModel, table=True):
    __tablename__ = "project_member"

    project_member_role_id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.user_id")
    project_id: int = Field(foreign_key="project.project_id")

    role_name: str

    # RELATIONSHIPS
    user: Optional["User"] = Relationship(back_populates="project_memberships")
    project: Optional["Project"] = Relationship(back_populates="members")
