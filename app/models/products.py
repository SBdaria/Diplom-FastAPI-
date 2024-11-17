from backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Product(Base):
    """
    info about product
    """
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    discription = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    cart = relationship('Cart', back_populates='product')
