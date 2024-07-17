from sqlalchemy import String, Column, Integer, ForeignKey
from database import Base, Engine #Base is a variable in database.py
from sqlalchemy.orm import relationship

class Product(Base):
  __tablename__ = 'products'

  id = Column(String(50), primary_key=True, index=True)
  category_id = Column(String(50), ForeignKey('categories.id'), unique=True)
  name = Column(String(50), unique=True)
  amount = Column(Integer)
  price = Column(Integer)
  created_at = Column(String(50))
  updated_at = Column(String(50))


class Category(Base):
  __tablename__ = 'categories'
    
  id = Column(String(50), primary_key=True, index=True)
  name = Column(String(50), unique=True)
  desc = Column(String(255))
  created_at = Column(String(50))
  updated_at = Column(String(50))


class Order(Base):
  __tablename__ = 'orders'
    
  id = Column(String(50), primary_key=True, index=True)
  customer_id = Column(String(50), ForeignKey('customers.id'), unique=True)
  created_at = Column(String(50))

  items = relationship('Product', back_populates='order')


class Customer(Base):
  __tablename__ = 'customers'

  id = Column(String(50), primary_key=True, index=True)
  name = Column(String(50), unique=True)
  phone = Column(String(15))
  age = Column(Integer)
  created_at = Column(String(50))
  updated_at = Column(String(50))
  
# Create the database tables
Base.metadata.create_all(bind=Engine)