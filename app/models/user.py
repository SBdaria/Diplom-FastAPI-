from backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    """
    info about user
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    phone = Column(String, nullable=False)
    birthday = Column(String, nullable=False)
    cart = relationship('Cart', back_populates='user')
