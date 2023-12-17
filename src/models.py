from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Integer, CheckConstraint('price > 0 AND price < 999999'), nullable=False)
    category = Column(String(50), nullable=False)
    views = Column(Integer, CheckConstraint('views >= 0'), default=0, nullable=False)
    path_to_img = Column(String, nullable=True)


