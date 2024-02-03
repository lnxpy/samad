import random

import pandas as pd
from fastapi import FastAPI, Request, Response, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from handler import connector

app = FastAPI()


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
def fake(user: User):

    df = pd.read_csv("meals.csv")
    meal = df.sample(n=1).squeeze()

    with open("qr.svg", "r") as file:
        qr = file.read()

    return {
        "primary": meal.to_dict(),
        "secondary": random.choice(["دوغ", "نوشابه", "پرتغال"]),
        "qrcode": qr,
        "ncode": random.randint(11111, 99999),
    }
