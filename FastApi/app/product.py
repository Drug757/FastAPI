from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    category: str
    price: float = Field(..., gt=0)
    quantity: int = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    sku: str

    # 1. Pydantic v2 Config: Позволяет работать с ORM-объектами
    model_config = {"from_attributes": True}
