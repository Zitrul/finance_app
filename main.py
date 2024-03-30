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
from functions import compare, CHECK_CHECKER, add_by_qr_info, get_history, auto_sort, auto_sort_vector, \
    get_current_price, get_current_price_trend
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


@app.post("/add_product_user")
def add_product(user_id: str, name: str, amount: str, category: str, currency: str, select_category: str):
    product = [Product(name, amount, currency, category)]
    if select_category == "True":
        product = auto_sort_vector(product)
    else:
        if product[0].category == "":
            product[0].category = "Остальное"
    db = DBmanager()
    db.add_products(product, int(user_id))
    db.commit()
    print(name, user_id)
    return {"OK": "OK"}


@app.post("/add_user_assets")
def add_user_assets(user_id: str, company_name: str, asset_amount: str, news_subscription: str, stock_quote: str):
    db = DBmanager()
    db.add_users_asset(company_name, news_subscription, user_id, asset_amount, stock_quote)
    db.commit()
    return {"OK": "OK"}


@app.get("/get_qr_info")
def add_user_assets(user_id: str, qr_data: str, auto_sort: str):
    response = add_by_qr_info(auto_change= auto_sort, user_id=int(user_id), qr_data= qr_data)
    return {"info": response}


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


@app.get("/get_users_subscription")
def get_users_subscription():
    db = DBmanager()
    subs = db.get_users_assets()
    db.commit()
    response = dict()
    response["subs"] = subs
    for i in subs:
        response["subs"].append(i[0])
    return response



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


@app.get("/get_history")
def get_history_method(ticker: str, date_from: str):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    result = get_history(ticket= ticker, date_end=current_date, date_start=date_from)
    return result


@app.get("/get_current_price")
def get_current_price_method(ticker: str):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    result = get_current_price(ticket= ticker, date_get=current_date)
    return result


@app.get("/get_current_price_trend")
def get_current_price_trend_method(ticker: str):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    result = get_current_price_trend(ticket= ticker, date_get=current_date)

    return result


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=3214)
