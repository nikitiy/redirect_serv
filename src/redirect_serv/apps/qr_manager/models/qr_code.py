from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import CHAR, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.redirect_serv.models import Base
from src.redirect_serv.models.mixins import IdMixin


class QRCode(IdMixin, Base):
    __tablename__ = "qr_codes"

    company_branch_id: Mapped[int] = mapped_column(
        ForeignKey("company_branches.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        unique=True,
    )
    qr_options: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB,
        default=dict,
        nullable=True,
    )
    url_hash: Mapped[str] = mapped_column(
        CHAR(64), nullable=False, unique=True, index=True
    )
    scan_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    last_scanned: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )

    # Relationships
    company_branch: Mapped["CompanyBranch"] = relationship(  # type: ignore
        back_populates="qr_code",
    )
