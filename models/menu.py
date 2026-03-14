from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, TIMESTAMP, BOOLEAN, NUMERIC, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class MenuORM(Base):
    __tablename__ = "menu_items"

    id_item = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String)
    price = Column(NUMERIC(10, 2), nullable=False)
    cost = Column(NUMERIC(10, 2))
    profit_margin = Column(NUMERIC(5, 2))
    is_available = Column(BOOLEAN, default=True)
    id_category = Column(Integer, ForeignKey("categories.id_category"))
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))

    category = relationship("CategoryORM", back_populates="menu_items")