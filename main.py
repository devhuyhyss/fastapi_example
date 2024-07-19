from fastapi import FastAPI, Query, Request, HTTPException, Depends
from pydantic import BaseModel, ValidationError, Field
from datetime import datetime
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Product, Category
from utils.common import paginate_query
from unidecode import unidecode
from typing import Optional
from sqlalchemy import and_

app = FastAPI()

class ProductItem(BaseModel):
  name: str
  category_id: str
  amount: int
  price: int
class ProductFilter(BaseModel):
  name: Optional[str] = Field(None, description="Product name")
  amount: Optional[int] = Field(None, ge=0, description="Product amount")
  price: Optional[int] = Field(None, ge=0, description="Product price") 

class CustomerItem(BaseModel):
  name: str
  phone: str
  age: int
  
# class OrderItem(BaseModel):
#   customer_id: str
#   products: list

class CategoryItem(BaseModel):
  name: str
  desc: str

def getDB():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# Product router
@app.get("/products")
async def getAllProduct(
  page: int = Query(default = 1),
  limit: int = Query(default = 1),
  name: str | None = None,
  price: int | None = None,
  amount: int | None = None,
  db: Session = Depends(getDB)
):
  filterParams = []
  if name:
    filterParams.append(Product.name.like(f"%{unidecode(name.lower())}%"))
  if price:
    filterParams.append(Product.price == price)
  if amount:
    filterParams.append(Product.amount == amount)

  query = db.query(Product).filter(and_(*filterParams))
  products = paginate_query(query, page, limit).all()
  return products

@app.post('/product')
async def createProduct(product: ProductItem, db: Session = Depends(getDB)):
  product = Product(
    name = product.name.strip(),
    category_id = product.category_id,
    amount = product.amount,
    price = product.price,
    created_at = datetime.now(),
    updated_at = datetime.now(),
  )
  db.add(product)
  db.commit()
  db.refresh(product)
  return product

@app.patch('/product/{id}')
async def updateProduct(product_update: ProductItem, id: str, db: Session = Depends(getDB)):
  product = db.query(Product).filter(Product.id == id).first()
  if not product:
    raise HTTPException(status_code=404, detail="Product not found")
  
  for key, value in product_update.dict(exclude_unset=True).items():
    setattr(product, key, value)
  product.updated_at = datetime.now()

  db.commit()
  db.refresh(product)
  return product

@app.delete('/product/{id}')
async def deleteProduct(id: str, db: Session = Depends(getDB)):
  product = db.query(Product).filter(Product.id == id).first()
  print(product)
  if product is None:
    raise HTTPException(status_code=404, detail="Product not found!")
  db.delete(product)
  db.commit()
  return {"message": "Product deleted success!"}



# Category router
@app.get("/categories")
async def getAllCategories(
  request: Request,
  page: int = Query(default= 1), limit: int = Query(default = 2), db: Session = Depends(getDB)):
  query_params = dict(request.query_params)

  query = db.query(Category)
  
  categories = paginate_query(query, page, limit).all()
  return categories

@app.post('/category')
async def createCategory(category: CategoryItem, db: Session = Depends(getDB)):
  category = Category(
    name = category.name.strip(),
    desc = category.desc.strip(),
    created_at = datetime.now(),
    updated_at = datetime.now(),
  )
  db.add(category)
  db.commit()
  db.refresh(category)
  return category

@app.patch('/category/{id}')
async def updateCategory(category_update: CategoryItem, id: str, db: Session = Depends(getDB)):
  category = db.query(Category).filter(Category.id == id).first()
  if not category:
    raise HTTPException(status_code=404, detail="Category not found")
  
  for key, value in category_update.dict(exclude_unset=True).items():
    setattr(category, key, value)
  category.updated_at = datetime.now()

  db.commit()
  db.refresh(category)
  return category

@app.delete('/category/{id}')
async def deleteCategory(id: str, db: Session = Depends(getDB)):
  category = db.query(Category).filter(Category.id == id).first()
  if category is None:
    raise HTTPException(status_code=404, detail="Category not found!")
  db.delete(category)
  db.commit()
  return {"message": "Category deleted success!"}



# Order router
# @app.get("/orders")
# async def getAllOrders(page: int = Query(default= 1), limit: int = Query(default=1), db: Session = Depends(getDB)):
#   query = db.query(Order)
#   orders = paginate_query(query, page, limit).all()
#   return orders

# @app.post('/order')
# async def createOrder(order: OrderItem, db: Session = Depends(getDB)):
#   order = Order(
#     customer_id = order.customer_id,
#     products = order.products,
#     created_at = datetime.now(),
#     updated_at = datetime.now(),
#   )
#   db.add(order)
#   db.commit()
#   db.refresh(order)
#   return order

# @app.delete('/order/{id}')
# async def deleteOrder(id: str, db: Session = Depends(getDB)):
#   order = db.query(Order).filter(Order.id == id).first()
#   if order is None:
#     raise HTTPException(status_code=404, detail="Order not found!")
#   db.delete(order)
#   db.commit()
#   return {"message": "Order deleted success!"}