import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from database.connection import Base

class UserORM(Base):
    __tablename__ = "users"

    id_user = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    phone = Column(String(20))
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))