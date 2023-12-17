from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Category(Enum):
    weapons = 'Weapons'
    knifes = 'Knifes'
    optics = 'Optics'
    medecine = 'Medicine'
    clothes = 'Clothes'


class ProductModel(BaseModel):
    name: str
    description: str
    price: int
    category: Category
    path_to_img: Optional[str] = None


class ProductReturnModel(ProductModel):
    id: int
    views: int
