from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    category: str
    discription: str
    price: int
    image_url: str
