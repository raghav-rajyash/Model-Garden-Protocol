from typing import List, Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship


class Organization(SQLModel, table=True):
    __tablename__ = "organization"

    organization_id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    onboarding_date: Optional[date] = None
    offload_date: Optional[date] = None
    subscription_validity_start_date: Optional[date] = None
    subscription_validity_end_date: Optional[date] = None
    contact_number: Optional[str] = None
    contact_email: Optional[str] = None
    contact_person_name: Optional[str] = None
    itomata_sales_representative: Optional[str] = None

    # RELATIONSHIP
    workspaces: List["Workspace"] = Relationship(back_populates="organization")
