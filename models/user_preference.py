from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.connection import Base

class UserPreferenceORM(Base):
    __tablename__ = "user_preferences"

    id_preference = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(UUID(as_uuid=True), ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False)
    preference_type = Column(String(100), nullable=False)
    preference_value = Column(String(150), nullable=False)
    confidence_score = Column(Numeric(3, 2), nullable=True)

    user = relationship("UserORM", back_populates="preferences")