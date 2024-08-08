from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from database import Base, Engine
from sqlalchemy.orm import relationship
from uuid import uuid4

class Product(Base):
  __tablename__ = 'products'

  id = Column(String(255), primary_key=True, default=uuid4)
  category_id = Column(String(255), ForeignKey('categories.id'))
  order_id = Column(String(255), ForeignKey('orders.id'))
  name = Column(String(255), unique=True)
  amount = Column(Integer)
  price = Column(Integer)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)


class Category(Base):
  __tablename__ = 'categories'
    
  id = Column(String(255), primary_key=True, default=uuid4)
  name = Column(String(255), unique=True)
  desc = Column(String(255))
  products = relationship('Product', backref='category', lazy=True)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)


class Order(Base):
  __tablename__ = 'orders'
    
  id = Column(String(255), primary_key=True, default=uuid4)
  customer_id = Column(String(255), ForeignKey('customers.id'), unique=True)
  products = relationship('Product', backref='order', lazy=True)
  created_at = Column(DateTime)


class Customer(Base):
  __tablename__ = 'customers'
    
  id = Column(String(255), primary_key=True, default=uuid4)
  name = Column(String(255), unique=True)
  address = Column(String(255))
  phone = Column(String(255))
  orders = relationship('Order', backref='customer', lazy=True)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)

# Create the database tables
Base.metadata.create_all(bind=Engine)