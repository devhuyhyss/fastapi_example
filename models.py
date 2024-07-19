from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from database import Base, Engine
from sqlalchemy.orm import relationship
from uuid import uuid4

class Product(Base):
  __tablename__ = 'products'

  id = Column(String, primary_key=True, default=uuid4)
  category_id = Column(String, ForeignKey('categories.id'), unique=True)
  name = Column(String, unique=True)
  amount = Column(Integer)
  price = Column(Integer)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)


class Category(Base):
  __tablename__ = 'categories'
    
  id = Column(String, primary_key=True, default=uuid4)
  name = Column(String, unique=True)
  desc = Column(String)
  products = relationship('Product', backref='category', lazy=True)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)


# class Order(Base):
#   __tablename__ = 'orders'
    
#   id = Column(String, primary_key=True, default=uuid4)
#   customer_id = Column(String, ForeignKey('customers.id'))
#   created_at = Column(DateTime)
#   products = relationship('Product', backref='order', lazy=True)


class Customer(Base):
  __tablename__ = 'customers'

  id = Column(String, primary_key=True, default=uuid4)
  name = Column(String, unique=True)
  phone = Column(String, unique=True)
  age = Column(Integer, unique=True)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)
  
# Create the database tables
Base.metadata.create_all(bind=Engine)