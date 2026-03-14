from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id_category = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String)

    menu_items = relationship("MenuORM", back_populates="category")