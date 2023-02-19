from dataclasses import dataclass

from sqlalchemy import Integer, String, Column

from chpass.dal.models.base import Base


@dataclass
class TopSite(Base):
    __tablename__ = 'top_sites'
    url = Column(String, primary_key=True)
    url_rank = Column(Integer)
    title = Column(String)
