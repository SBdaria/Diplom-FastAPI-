from fastapi import FastAPI, Request, Depends, Form
from typing import Annotated
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import Product, User, Cart
from sqlalchemy import insert, select
from routers import products, users
from datetime import datetime

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), 'static')
templates = Jinja2Templates(directory='templates')


@app.get('/')
async def homepage(request: Request):
    context = {'request': request, 'namepage': 'homepage', 'title': 'Главная страница'}
    return templates.TemplateResponse(name='mainpages/homepage.html', context=context)


@app.get('/catalog')
async def catalog(request: Request):
    context = {'request': request, 'namepage': 'catalog', 'title': 'Каталог'}
    return templates.TemplateResponse(name='mainpages/catalog.html', context=context)


@app.get('/about')
async def about(request: Request):
    context = {'request': request, 'namepage': 'about', 'title': 'О нас'}
    return templates.TemplateResponse(name='mainpages/about_us.html', context=context)


@app.get('/info')
async def info(request: Request):
    context = {'request': request, 'namepage': 'info', 'title': 'Доставка и оплата'}
    return templates.TemplateResponse(name='mainpages/info.html', context=context)


@app.get('/jackets')
async def jackets(request: Request, db: Annotated[Session, Depends(get_db)]):
    jackets = db.query(Product).filter(Product.category == 'jackets').all()
    context = {'request': request, 'namepage': 'jackets', 'category': 'Куртки', 'type_cloth': jackets}
    return templates.TemplateResponse(name='mainpages/catalogpage.html', context=context)


@app.get('/tshirts')
async def tshirts(request: Request, db: Annotated[Session, Depends(get_db)]):
    tshirts = db.query(Product).filter(Product.category == 'tshirts').all()
    context = {'request': request, 'namepage': 'tshirts', 'category': 'Футболки', 'type_cloth': tshirts}
    return templates.TemplateResponse(name='mainpages/catalogpage.html', context=context)


@app.get('/hoodies')
async def hoodies(request: Request, db: Annotated[Session, Depends(get_db)]):
    hoodies = db.query(Product).filter(Product.category == 'hoodies').all()
    context = {'request': request, 'namepage': 'hoodies', 'category': 'Худи', 'type_cloth': hoodies}
    return templates.TemplateResponse(name='mainpages/catalogpage.html', context=context)


@app.get('/jeans')
async def jeans(request: Request, db: Annotated[Session, Depends(get_db)]):
    jeans = db.query(Product).filter(Product.category == 'jeans').all()
    context = {'request': request, 'namepage': 'jeans', 'category': 'Джинсы', 'type_cloth': jeans}
    return templates.TemplateResponse(name='mainpages/catalogpage.html', context=context)


@app.get('/shoes')
async def shoes(request: Request, db: Annotated[Session, Depends(get_db)]):
    shoes = db.query(Product).filter(Product.category == 'shoes').all()
    context = {'request': request, 'namepage': 'shoes', 'category': 'Кроссовки и кеды', 'type_cloth': shoes}
    return templates.TemplateResponse(name='mainpages/catalogpage.html', context=context)


@app.get('/cart/{cloth_id}')
async def cart_info(request: Request, db: Annotated[Session, Depends(get_db)], cloth_id: int):
    cloth = db.scalar(select(Product).where(Product.id == cloth_id))
    context = {'request': request, 'namepage': 'shoes', 'title': 'Подтверждение заказа', 'cloth': cloth}
    return templates.TemplateResponse(name='mainpages/cart_info.html', context=context)


@app.post("/cart_info/{cloth_id}")
async def cart_order(request: Request, db: Annotated[Session, Depends(get_db)],
                     cloth_id: int,
                     username: str = Form(),
                     password: str = Form()):
    """
    function that is triggered
    when the "confirm" button is clicked on a cart_info page
    and verifies the data entered by the user
    :param cloth_id: id of the product that the user selected
    :param username, password: info about user from the page
    :return: page template and message about the result of data verification
    """
    cloth = db.scalar(select(Product).where(Product.id == cloth_id))
    context = {'request': request, 'cloth': cloth}
    user_find = db.scalar(select(User).where(User.username == username))
    if not user_find:
        context.update({
            'namepage': 'shoes',
            'title': 'Подтверждение заказа',
            'message': 'Такой пользователь не зарегистрирован!'
        })
        return templates.TemplateResponse(name='mainpages/cart_info.html', context=context)

    if password != user_find.password:
        context.update({
            'namepage': 'shoes',
            'title': 'Подтверждение заказа',
            'message': 'Пароли не совпадают!'
        })
        return templates.TemplateResponse(name='mainpages/cart_info.html', context=context)
    db.execute(insert(Cart).values(date_order=datetime.now().strftime('%Y-%m-%d %H:%M'),
                                   user_id=user_find.id,
                                   product_id=cloth_id))
    db.commit()
    context.update({
        'namepage': 'submit_order',
        'title': 'Ваш заказ успешно подтвержден'
    })
    return templates.TemplateResponse(name='mainpages/submit_order.html', context=context)


app.include_router(products.router)
app.include_router(users.router)
