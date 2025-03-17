import os
import json
from typing import List, Dict, Optional, Union

from fastapi import FastAPI, Depends, HTTPException
import uvicorn
import requests
from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship, Column, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse

# Load environment variables
DB_PASSWORD = os.getenv("DB_PASSWORD", "Mrin@0108")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_NAME = os.getenv("DB_NAME", "PRODUCTS")
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Encode password
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"

# Database setup
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize FastAPI
app = FastAPI()

def create_database():
    temp_engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{encoded_password}@{DB_HOST}")
    conn = temp_engine.raw_connection()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()
    conn.close()
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_database()

# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLModel schemas
class Dimensions(SQLModel):
    width: float
    height: float
    depth: float

class Review(SQLModel):
    rating: int
    comment: str
    date: datetime
    reviewer_name: str
    reviewer_email: str

class Meta(SQLModel):
    created_at: datetime
    updated_at: datetime
    barcode: str
    qr_code: str

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    category: str
    price: float
    discount_percentage: float = Field(alias="discountPercentage")
    rating: float
    stock: int
    tags: List[str] = Field(sa_column=Column(JSON))
    brand: str
    sku: str
    weight: float
    dimensions: Dict = Field(sa_column=Column(JSON))  # Storing as JSON
    warranty_information: str = Field(alias="warrantyInformation")
    shipping_information: str = Field(alias="shippingInformation")
    availability_status: str = Field(alias="availabilityStatus")
    reviews: List[Dict] = Field(sa_column=Column(JSON))  # Storing as JSON
    return_policy: str = Field(alias="returnPolicy")
    minimum_order_quantity: int = Field(alias="minimumOrderQuantity")
    meta: Dict = Field(sa_column=Column(JSON))  # Storing as JSON
    images: List[str] = Field(sa_column=Column(JSON))
    thumbnail: str

# Fetch data from API
def fetch_data():
    response = requests.get("https://dummyjson.com/products")
    return response.json()

@app.get("/")
def read_root():
    data = fetch_data()
    return data

@app.get("/filter/{item_price}")
async def filter_items(item_price: int, data: dict = Depends(fetch_data)):
    filtered_data = [product for product in data['products'] if product['price'] >= item_price]
    return filtered_data

@app.post("/products/")
def add_product(product: Product, db: Session = Depends(get_db)) -> Dict:
    """
    Adds a product to the database.
    """
    #
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added successfully", "product": new_product}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
