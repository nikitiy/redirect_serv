from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.redirect_serv.models import Base
from src.redirect_serv.models.mixins import IdMixin


class Company(IdMixin, Base):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    subdomain: Mapped[str] = mapped_column(
        String(63),
        unique=True,
        index=True,
    )

    # Relationships
    branches: Mapped[List["CompanyBranch"]] = relationship(  # type: ignore
        back_populates="company",
        cascade="all, delete-orphan",
    )
