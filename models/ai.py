from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from database.connection import Base

class AIORM(Base):
    __tablename__ = "ai_interactions"

    id_interaction = Column(Integer, primary_key=True)
    id_user = Column(UUID(as_uuid=True), ForeignKey("users.id_user"), nullable=False)
    input_text = Column(String, nullable=False)
    parsed_intent = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("UserORM", back_populates="ai_interactions")