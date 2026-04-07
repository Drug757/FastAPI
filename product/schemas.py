from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    price: int = Field(..., ge=0)
    in_stock: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductFilterParams(BaseModel):
    min_price: Optional[int] = Field(None, ge=0)
    max_price: Optional[int] = Field(None, ge=0)
    in_stock: Optional[bool] = None

    @field_validator('max_price')
    def validate_price_range(cls, v, info):
        if v is not None and info.data.get('min_price') is not None:
            if info.data['min_price'] > v:
                raise ValueError('min_price не может быть больше max_price')
        return v