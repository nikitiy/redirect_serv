from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.redirect_serv.models import Base
from src.redirect_serv.models.mixins import IdMixin


class CompanyBranch(IdMixin, Base):
    __tablename__ = "company_branches"

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )

    # Relationships
    company: Mapped["Company"] = relationship(  # type: ignore
        back_populates="branches",
    )
    qr_code: Mapped[Optional["QRCode"]] = relationship(  # type: ignore
        back_populates="company_branch",
        uselist=False,
    )
