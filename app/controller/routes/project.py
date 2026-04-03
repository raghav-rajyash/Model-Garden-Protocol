from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.model import Project, User
from app.view.project import ProjectRead
from app.controller.routes.auth import get_current_user

router = APIRouter(tags=["projects"])

@router.get("/", response_model=List[ProjectRead])
async def list_user_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    projects = await Project.get_by_user(db, current_user.user_id)
    return projects
