from fastapi import APIRouter
from app.controller.routes.auth import router as auth_router
from app.controller.routes.project import router as project_router
from app.controller.routes.model import router as model_router


v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(project_router, prefix="/projects")
v1_router.include_router(model_router)

# Export as router for main.py import from app.controller
router = v1_router
