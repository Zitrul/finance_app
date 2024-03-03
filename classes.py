from fastapi import UploadFile
from pydantic import BaseModel
class stringa(BaseModel):
    name: str

class Product:
    def __init__(self, name, amount, currency, category):
        self.price = amount
        self.currency = currency
        self.category = category
        self.name = name
