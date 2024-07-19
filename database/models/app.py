from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from utils.enums import StateEnum

from .base import BaseModel


class AppModel(BaseModel):
    __tablename__ = "apps"

    app_id: Mapped[UUID] = mapped_column(primary_key=True, unique=True, default=uuid4, index=True)
    kind: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(nullable=False, default="")
    version: Mapped[str] = mapped_column(nullable=False, default="")
    description: Mapped[str] = mapped_column(nullable=False, default="")
    state: Mapped[StateEnum] = mapped_column(nullable=False, default="NEW")
    json: Mapped[dict] = mapped_column(JSON, nullable=True)

    __table_args__ = (
        CheckConstraint("char_length(kind) <= 32", name="kind_length_check"),
        CheckConstraint("char_length(name) <= 128", name="name_length_check"),
        CheckConstraint("char_length(description) <= 4096", name="description_length_check"),
        CheckConstraint(
            "version ~ '^\\d+\\.\\d+\\.\\d+$'",
            name="version_format_check",
        ),
    )
