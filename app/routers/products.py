from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from sqlalchemy import insert, select, delete
from schemas import CreateProduct
from models import Product

router = APIRouter(prefix='/product', tags=['product'])


@router.post("/upload_foto")
async def create_upload_foto(uploaded_foto: UploadFile = File(...)):
    """
    function for loading product's image into the project
    :param uploaded_foto: image of product
    :return: dict with status code and message
    """
    foto = await uploaded_foto.read()
    with open(f'static/images/{uploaded_foto.filename}', 'wb') as file:
        file.write(foto)
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.post('/create')
async def create_product(db: Annotated[Session, Depends(get_db)], create_product: CreateProduct):
    """
    function for loading information about product into the database
    :param db: database with info about products
    :param create_product: model of product
    :return: dict with status code and message
    """
    db.execute(insert(Product).values(name=create_product.name,
                                      category=create_product.category,
                                      discription=create_product.discription,
                                      price=create_product.price,
                                      image_url=create_product.image_url))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.delete('/delete')
async def delete_product(db: Annotated[Session, Depends(get_db)], product_id: int):
    """
    function for deleting information about product from the database
    :param db: database with info about products
    :param product_id: product's id
    :return: dict with status code and message
    """
    product = db.scalar(select(Product).where(Product.id == product_id))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product was not found'
        )

    db.execute(delete(Product).where(Product.id == product_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful'
    }
