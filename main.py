import datetime
from typing import Union
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi import UploadFile, File, Form

from DBmanager import DBmanager
from functions import CHECK_CHECKER, auto_sort
from classes import stringa, Product

app = FastAPI()


@app.get("/")
def read_main(name : stringa):
    print(name)
    return {"Hello": "World"}
@app.get("/add_product_user")
def add_product(user_id: str, name: str, amount: str, category: str, currency: str, select_category: str):
    product = [Product(name, amount, currency, category)]
    if select_category == "True":
        product = auto_sort(product)
    else:
        if product[0].category == "":
            product[0].category = "Остальное"
    db = DBmanager()
    db.add_products(product, int(user_id))
    db.commit()
    print(name, user_id)
    return {"OK": "OK"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
@app.post("/check_check")
async def create_upload_file(uploaded_file: UploadFile = File(), user_id: str = Form(), sort: str = Form()):
    user_id = int(user_id)
    if sort == "True":
        sort = True
    else:
        sort = False

    file_location = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + uploaded_file.filename

    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    result = CHECK_CHECKER(sort, user_id, file_location)
    return {"info": result}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
