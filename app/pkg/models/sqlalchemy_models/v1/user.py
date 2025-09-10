"""SQlAlchemy model for user."""

import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.pkg.models.sqlalchemy_models import Base
from app.pkg.models.v1 import ServiceRoleEnum


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    user_name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    user_is_active: Mapped[bool] = mapped_column(default=True)
    user_is_verified: Mapped[bool] = mapped_column(default=False)
    user_service_role: Mapped[ServiceRoleEnum] = mapped_column(
        SQLEnum(ServiceRoleEnum, name="service_role_enum", native_enum=False),
        default=ServiceRoleEnum.USER,
        nullable=False,
    )
    user_create_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    user_update_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())
