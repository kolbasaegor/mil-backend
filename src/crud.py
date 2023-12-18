from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import desc

from .models import Product
from .schemas import ProductModel, ProductReturnModel


def get_all_poducts(session: Session) -> List[ProductReturnModel]:
    return session.query(Product).all()


def get_product_by_id(session: Session, id: int):
    return session.query(Product).filter(Product.id == id).one_or_none()


def add_product(session: Session, product: ProductModel) -> ProductReturnModel:
    new_product = Product(
        name = product.name,
        description = product.description,
        price = product.price,
        category = product.category.value,
        views=0,
        path_to_img = product.path_to_img
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product


def increase_views(session: Session, id: int) -> int:
    updated_product = session.query(Product).filter(Product.id == id).one_or_none()

    if not updated_product:
        return -1
    
    updated_product.views += 1

    session.commit()
    session.refresh(updated_product)

    return updated_product.views


def get_top_products(session: Session, limit: int = 10) -> List[ProductReturnModel]:
    return session.query(Product).order_by(desc(Product.views)).limit(limit).all()


def remove_product(session: Session, id: int) -> ProductReturnModel:
    product = session.query(Product).filter(Product.id == id).one_or_none()

    session.delete(product)
    session.commit()

    return product   
