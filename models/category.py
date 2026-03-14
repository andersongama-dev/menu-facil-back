from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database.connection import Base

class CategoryORM(Base):
    __tablename__ = "categories"

    id_category = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String)

    menu_items = relationship("MenuORM", back_populates="category")