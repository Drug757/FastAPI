from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_name(db: Session, name: str):
    return db.query(Product).filter(Product.name == name).first()

def get_products(db: Session, skip: int = 0, limit: int = 100, 
                 min_price: int = None, max_price: int = None, 
                 in_stock: bool = None):
    query = db.query(Product)
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if in_stock is not None:
        query = query.filter(Product.in_stock == in_stock)
    
    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        price=product.price,
        in_stock=product.in_stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db_product.in_stock = product.in_stock
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False