import os
import random
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from handler import connector

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


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
def fake(user: User, request: Request):
    df = pd.read_csv("meals.csv")
    meal = df.sample(n=1).squeeze()

    base_url = str(request.base_url).split("://")[1]
    static_path = Path("static")
    file_path = base_url / static_path / "qr.png"

    return {
        "primary": meal.to_dict(),
        "secondary": random.choice(["دوغ", "نوشابه", "پرتغال"]),
        "qrcode": file_path,
        "ncode": random.randint(11111, 99999),
        "name": "ابوالفضل سلیمانی",
        "wallet": f"{random.randint(1, 10) * 4500:,}",
    }
