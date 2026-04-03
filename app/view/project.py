from typing import Optional
from pydantic import BaseModel

class ProjectBase(BaseModel):
    project_name: str
    project_status: str
    project_category: str = "my-projects"
    project_credits: int = 0

class ProjectCreate(ProjectBase):
    workspace_id: int

class ProjectRead(ProjectBase):
    project_id: int
    workspace_id: int

    class Config:
        from_attributes = True
