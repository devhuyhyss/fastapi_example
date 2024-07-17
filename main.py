from fastapi import FastAPI, Query, Request, HTTPException, Depends
import uuid
from pydantic import BaseModel
from datetime import datetime
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Product, Category, Customer, Order
import uvicorn

app = FastAPI()

class ProductItem(BaseModel):
  name: str
  category_id: str
  amount: int
  price: int

class CustomerItem(BaseModel):
  name: str
  category_id: str
  amount: int
  price: int
  
class OrderItem(BaseModel):
  name: str
  category_id: str
  amount: int
  price: int

class CategoryItem(BaseModel):
  name: str
  desc: str

def getDB():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# Get methods tables
@app.get("/products")
async def getAllProduct(db: Session = Depends(getDB)):
  products = db.query(Product).all()
  return products

@app.get("/orders")
async def getAllOrders(db: Session = Depends(getDB)):
  orders = db.query(Order).all()
  return orders

@app.get("/customers")
async def getAllCustomers(db: Session = Depends(getDB)):
  customers = db.query(Customer).all()
  return customers

@app.get("/categories")
async def getAllCategories(db: Session = Depends(getDB)):
  categories = db.query(Category).all()
  return categories


# Create methods tables
@app.post('/product')
async def createProduct(product: ProductItem, db: Session = Depends(getDB)):
  product = Product(
    id = uuid.uuid4(),
    name = product.name.strip(),
    category_id = product.category_id,
    amount = product.amount,
    price = product.price,
    created_at = str(datetime.now()),
    updated_at = str(datetime.now()),
  )
  db.add(product)
  db.commit()
  db.refresh(product)
  return product

@app.post('/category')
async def createCategory(category: CategoryItem, db: Session = Depends(getDB)):
  category = Category(
    id = uuid.uuid4(),
    name = category.name.strip(),
    desc = category.desc.strip(),
    created_at = str(datetime.now()),
    updated_at = str(datetime.now()),
  )
  db.add(category)
  db.commit()
  db.refresh(category)
  return category


if __name__ == "__main__":
  uvicorn.run('main:app', reload=True)