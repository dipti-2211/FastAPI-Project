from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import engine, Base, get_db, SessionLocal
from models import ProductDB, ProductCreate, ProductResponse

# Create tables in the SQLite database automatically on startup
Base.metadata.create_all(bind=engine)

# Seed demo data if database is empty
def seed_demo_data():
    db = SessionLocal()
    try:
        if db.query(ProductDB).first() is None:
            demo_products = [
                ProductDB(id=1, name="Laptop", description="High performance laptop", price=1000.0, quantity=10),
                ProductDB(id=2, name="Mouse", description="Wireless optical mouse", price=200.0, quantity=25),
                ProductDB(id=3, name="Keyboard", description="Mechanical keyboard", price=300.0, quantity=15),
                ProductDB(id=4, name="Key", description="Replacement keycap set", price=30.0, quantity=50),
                ProductDB(id=5, name="USB_cable", description="Type-C charging cable", price=300.0, quantity=40),
            ]
            db.add_all(demo_products)
            db.commit()
    finally:
        db.close()

seed_demo_data()

app = FastAPI()

# Enable CORS for the React frontend (running on http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def greet():
    return {"message": "hi This is demo work"}

# Get all products
@app.get("/products", response_model=List[ProductResponse])
@app.get("/products/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductDB).all()

# Get a product by ID
@app.get("/products/{id}", response_model=ProductResponse)
@app.get("/products/{id}/", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found !!")
    return product

# Add a product (supports user-provided ID or auto-generated ID)
@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
@app.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(prod: ProductCreate, db: Session = Depends(get_db)):
    if prod.id is not None:
        existing = db.query(ProductDB).filter(ProductDB.id == prod.id).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Product with ID {prod.id} already exists")
        db_product = ProductDB(
            id=prod.id,
            name=prod.name,
            description=prod.description or "",
            price=prod.price,
            quantity=prod.quantity
        )
    else:
        db_product = ProductDB(
            name=prod.name,
            description=prod.description or "",
            price=prod.price,
            quantity=prod.quantity
        )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Update a product
@app.put("/products/{id}", response_model=ProductResponse)
@app.put("/products/{id}/", response_model=ProductResponse)
def update_product(id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found !!")
    
    db_product.name = product.name
    db_product.description = product.description or ""
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product)
    return db_product

# Delete a product
@app.delete("/products/{id}")
@app.delete("/products/{id}/")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found !!")
    
    db.delete(db_product)
    db.commit()
    return {"message": "deleted Successfully"}

