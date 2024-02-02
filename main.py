import random
from test import connector

from fastapi import FastAPI, Request, Response, status
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    username: str
    password: str


@app.post("/", status_code=status.HTTP_200_OK)
def main(user: User, response: Response):
    try:
        content = connector(user.username, user.password)
        return content
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        print(e)
        return {}


@app.post("/fake/")
async def create_item(user: User):
    with open("meals.txt", "r") as file:
        meals = [i.strip("\n") for i in file.readlines()]
    with open("qr.svg", "r") as file:
        qr = file.read()
    return {
        "primary": random.choice(meals),
        "secondary": random.choice(["دوغ", "نوشابه", "پرتغال"]),
        "qrcode": qr,
        "ncode": random.randint(11111, 99999),
    }
