from fastapi import UploadFile
from pydantic import BaseModel
class stringa(BaseModel):
    name: str

class Product:
    def __init__(self, name, price, quantity, cost, category):
        self.price = price
        self.quantity = quantity
        self.cost = cost
        self.category = category
        self.name = name
