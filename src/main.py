from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import create_tables, get_session
from .schemas import ProductModel, ProductReturnModel
from . import crud


app = FastAPI(
    title='Backend for epja project'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie","Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)


@app.on_event("startup")
async def startup_event():
    create_tables()


@app.get('/')
def greeting():
    return {
        'msg': 'Backend for EPJA project',
        'version': '0.1.0',
        'endpoints': [
            '/products/get-all',
            '/products/get-one',
            '/products/get-top',
            '/products/increase-views',
            '/products/get-many',
            '/products/add',
            '/products/remove'
        ] 
    }


@app.get('/products/get-all')
def get_products(session: Session = Depends(get_session)) -> List[ProductReturnModel]:
    return crud.get_all_poducts(session)


@app.get('/products/get-one')
def get_one_product(id: int, session: Session = Depends(get_session)):
    return crud.get_product_by_id(session, id)


@app.get('/products/get-top')
def get_top_products(limit: int = 10, session: Session = Depends(get_session)) -> List[ProductReturnModel]:
    return crud.get_top_products(session, limit)


@app.get('/products/increase-views')
def increase_views(id: int, session: Session = Depends(get_session)) -> int:
    new_views = crud.increase_views(session, id)

    if new_views == -1:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return new_views


@app.post('/products/get-many')
def get_many_products(ids: List[int], session: Session = Depends(get_session)):
    products = [crud.get_product_by_id(session, id) for id in ids]
    return products


@app.post('/products/add')
def add_product(product: ProductModel, session: Session = Depends(get_session)) -> ProductReturnModel:
    return crud.add_product(session, product)


@app.delete('/products/remove')
def remove_product(id: int, session: Session = Depends(get_session)) -> ProductReturnModel:
    product = crud.get_product_by_id(session, id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return crud.remove_product(session, id)
