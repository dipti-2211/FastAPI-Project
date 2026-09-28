from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, String
from database import Base

# --- SQLAlchemy Database Table ---
class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)


# --- Pydantic Schemas (API validation) ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = ""
    price: float
    quantity: int

class ProductCreate(ProductBase):
    id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True

