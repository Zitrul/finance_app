import datetime
from typing import Union
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi import UploadFile, File, Form
import base64
from threading import Thread
from io import BytesIO
from PIL import Image
from DBmanager import DBmanager
from functions import CHECK_CHECKER, auto_sort
from classes import stringa, Product

first_time_tg = ""
first_time = ""
app = FastAPI()


def write(base64_data):
    import base64
    from io import BytesIO
    from PIL import Image
    bytes_data = base64.b64decode(base64_data)
    image_bytes = BytesIO(bytes_data)

    image = Image.open(image_bytes)
    file_location = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.png'
    image.save(file_location)
    return file_location


@app.get("/")
def read_main(name: str):
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


@app.get("/get_last_news_tg")
def get_last_news_tg():
    db = DBmanager()
    news = db.search_for_news()
    db.commit()
    response = dict()
    need_to_delete = []
    for i in news:
        need_to_delete.append(i[0])
        response[i[0]] = dict()
        response[i[0]]["title"] = i[1]
        response[i[0]]["date"] = i[4]
        response[i[0]]["link"] = i[2]
        response[i[0]]["description"] = i[3]
    db = DBmanager()
    db.update_news(need_to_delete)
    db.commit()
    return response


@app.post("/uploadfile/")
async def create_upload_file(data: str):
    print(data)
    with open('image.jpeg', "wb+") as file_object:
        file_object.write(data.encode('utf-8'))
    return {"filename": 'ok'}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/check_bill")
def create_upload_file_2(base64_data: str = Form(), user_id: str = Form(), sort: str = Form()):
    from PIL import Image
    bytes_data = base64.b64decode(base64_data)
    image_bytes = BytesIO(bytes_data)

    image = Image.open(image_bytes)
    file_location = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.png'
    image.save(file_location)
    user_id = int(user_id)
    if sort == "True":
        sort = True
    else:
        sort = False

    result = CHECK_CHECKER(sort, user_id, file_location)
    return {"info": result}


@app.post("/check_check")
async def create_upload_file(uploaded_file: UploadFile = File(), user_id: str = Form(), sort: str = Form()):
    print(uploaded_file)
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

    first_time = str(str(datetime.date.today()).replace("-", ".")) + " " + str(datetime.datetime.now().time()).split(".")[0]
    first_time_tg = str(str(datetime.date.today()).replace("-", ".")) + " " + str(datetime.datetime.now().time()).split(".")[0]
    uvicorn.run(app, host="0.0.0.0", port=3214)
