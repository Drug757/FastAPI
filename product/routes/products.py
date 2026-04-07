from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from crud import (
    get_product, get_product_by_name, get_products,
    create_product, update_product, delete_product
)
from schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    existing_product = get_product_by_name(db, product.name)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists"
        )
    return create_product(db, product)

@router.get("/", response_model=list[ProductResponse])
def list_products(
    min_price: Optional[int] = Query(None, ge=0, description="Минимальная цена"),
    max_price: Optional[int] = Query(None, ge=0, description="Максимальная цена"),
    in_stock: Optional[bool] = Query(None, description="Фильтр по наличию"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price cannot be greater than max_price"
        )
    
    products = get_products(
        db, skip=skip, limit=limit,
        min_price=min_price, max_price=max_price, in_stock=in_stock
    )
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int, 
    product: ProductUpdate, 
    db: Session = Depends(get_db)
):
    existing = get_product(db, product_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if existing.name != product.name:
        name_exists = get_product_by_name(db, product.name)
        if name_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this name already exists"
            )
    
    updated = update_product(db, product_id, product)
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    delete_product(db, product_id)
    return None