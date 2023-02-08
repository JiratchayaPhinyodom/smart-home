from fastapi import FastAPI, Body
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient

load_dotenv(".env")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
DB_URL = "mongodb://{}:{}@mongo.exceed19.online:{}".format(USER, PASSWORD, PORT)
client =  MongoClient(DB_URL)
db = client["exceed05"]
bulb_collecton = db["smart-home"]


class Bulb(BaseModel):
    bulb_id: int
    is_auto_or_manual: Optional[int]
    is_it_open: int


app = FastAPI()

@app.get("/")
def root():
    return {"Hi": "world"}



def get_all_bulb_status():
    bulbs = bulb_collecton.find({}, {"_id": 0})
    return list(bulbs)

@app.post("/switch")
def switch_on(bulb: Bulb = Body()):
    pass
     




