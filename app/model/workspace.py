from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, ForeignKey


class Workspace(SQLModel, table=True):
    __tablename__ = "workspace"

    workspace_id: Optional[int] = Field(default=None, primary_key=True)

    workspace_owner_id: int = Field(foreign_key="user.user_id")
    workspace_organization_id: int = Field(foreign_key="organization.organization_id")
    workspace_subscription_id: Optional[str] = None
    workspace_name: str

    # RELATIONSHIPS
    organization: Optional["Organization"] = Relationship(back_populates="workspaces")
    owner: Optional["User"] = Relationship(back_populates="owned_workspaces")
    projects: List["Project"] = Relationship(back_populates="workspace")
