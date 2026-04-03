from sqlalchemy.ext.asyncio import AsyncSession
from app.model import User, Organization, Workspace, Project
from sqlmodel import select, delete

async def seed_for_test_user(session: AsyncSession, user: User):
    # Check if we already seeded for this user to avoid performance hit on every login
    # But for a "seed" behavior after DB deletion, it's fine.
    
    # Ensure organization exists
    statement = select(Organization).where(Organization.name == "Test Org")
    result = await session.execute(statement)
    org = result.scalar_one_or_none()
    
    if not org:
        org = Organization(name="Test Org")
        session.add(org)
        await session.flush()
        
    # Ensure workspace exists
    statement = select(Workspace).where(Workspace.workspace_owner_id == user.user_id)
    result = await session.execute(statement)
    workspace = result.scalar_one_or_none()
    
    if not workspace:
        workspace = Workspace(
            workspace_owner_id=user.user_id,
            workspace_organization_id=org.organization_id,
            workspace_name="Main Workspace"
        )
        session.add(workspace)
        await session.flush()

    # If workspace has projects, don't seed again (prevent duplicate data)
    statement = select(Project).where(Project.workspace_id == workspace.workspace_id)
    result = await session.execute(statement)
    existing_projects = result.scalars().first()
    
    if existing_projects:
        return

    # Projects to create (Name, Status, Category)
    projects_data = [
        ("Generic Drug Suggester", "Daft", "my-projects"),
        ("Contact Center", "Draft", "my-projects"),
        ("Learning Assistant", "Hosted", "my-projects"),
        ("Thesis Guide", "Under Tuning", "my-projects"),
        
        ("Apartment Designer", "Daft", "collab"),
        ("The Visual Inspector", "Draft", "collab"),
        ("Insurance Agent", "Hosted", "collab"),
        ("Smart CAM", "Under Tuning", "collab"),
        
        ("POS BOT", "Daft", "reviews"),
        ("Service Engineer Trainer", "Draft", "reviews"),
        ("The AI Journal Builder", "Hosted", "reviews"),
        ("My Media House", "Under Tuning", "reviews"),
        
        ("POS BOT", "Daft", "trainings"),
        ("Service Engineer Trainer", "Draft", "trainings"),
        ("The AI Journal Builder", "Hosted", "trainings"),
        ("My Media House", "Under Tuning", "trainings"),
    ]
    
    for p_name, p_status, p_category in projects_data:
        project = Project(
            project_name=p_name,
            project_status=p_status,
            project_category=p_category,
            workspace_id=workspace.workspace_id
        )
        session.add(project)
    
    await session.commit()
