from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250))
    stock_quantity = Column(Integer, nullable=False, default=0, server_default="0")