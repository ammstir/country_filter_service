from sqlalchemy import ARRAY, Column, DateTime, String, func

from src.models.base import Base


class IsoCountries(Base):
    __tablename__ = "iso_countires"

    iso_code = Column(String(3), primary_key=True)
    names = Column(ARRAY(String), nullable=False)
    last_updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())
