from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, NUMERIC, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.connection import Base


class OrderORM(Base):
    __tablename__ = "orders"

    id_order = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(UUID(as_uuid=True), ForeignKey("users.id_user"))
    total_price = Column(NUMERIC(10, 2))
    status = Column(String(50), default="pending")
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("UserORM", back_populates="orders")