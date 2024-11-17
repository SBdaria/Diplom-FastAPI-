from backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Cart(Base):
    """
    user order information
    """
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, index=True)
    date_order = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    user = relationship('User', back_populates='cart')
    product = relationship('Product', back_populates='cart')
