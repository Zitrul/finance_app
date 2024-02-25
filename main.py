import datetime
from typing import Union
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi import UploadFile, File, Form
from functions import CHECK_CHECKER
from classes import stringa
app = FastAPI()


@app.get("/")
def read_main(name : stringa):
    print(name)
    return {"Hello": "World"}


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
    file_location = f"{datetime.datetime.now()}{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    result = CHECK_CHECKER(sort, user_id, file_location)
    return {"info": result}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
