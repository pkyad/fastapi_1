from db.meta import meta, Model
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional


class Tenant(Model):
    __tablename__ = "shared_tenant"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    expiry_date: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean)
    users: Mapped[list["Administrator"]] = relationship(back_populates="tenant")


class Administrator(Model):
    __tablename__ = "shared_administrator"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    mobile: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    next_password_change_due: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean)
    is_staff: Mapped[bool] = mapped_column(Boolean)
    is_admin: Mapped[bool] = mapped_column(Boolean)
    password_change_required: Mapped[bool] = mapped_column(Boolean)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("shared_tenant.id"))
    tenant: Mapped["Tenant"] = relationship(back_populates="users")


class AdministratorT(BaseModel):
    id: int
    name: str
    email: str
    mobile: Optional[str]
    is_active: bool
    is_admin: bool
    is_staff: bool
    password_change_required: bool
    next_password_change_due: Optional[str]
    tenant: Optional["TenantT"]


class TenantT(BaseModel):
    id: int
    name: str
    is_active: bool
    expiry_date: Optional[str]
    users: list["AdministratorT"]


TenantT.update_forward_refs()
AdministratorT.update_forward_refs()
