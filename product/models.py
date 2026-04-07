from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    in_stock = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, in_stock={self.in_stock})>"