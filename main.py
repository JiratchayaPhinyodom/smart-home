from fastapi import FastAPI, Body, HTTPException
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
load_dotenv(".env")

USER = os.getenv("username")
PASSWORD = os.getenv("password")
client = MongoClient(f"mongodb://{USER}:{PASSWORD}@mongo.exceed19.online:8443/?authMechanism=DEFAULT")

db = client["exceed05"]
bulb_collecton = db["smart-home"]


class Bulb(BaseModel):
    bulb_id: int
    is_auto_or_manual: Optional[int]
    is_it_open: int


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Hi": "world"}


#Front
def get_all_bulb_status():
    bublbs = bulb_collecton.find({}, {"_id":False})
    return list(bublbs)
    

#Front send data to back when user interact on webpage
@app.post("/front/request")
def collect_data(bulb: Bulb = Body()):
    bulbs = bulb_collecton.find({"bulb_id":bulb.bulb_id}, {"_id": False})
    if bulbs:
        bulb_collecton.update_one({"bulb_id": bulb.bulb_id}, 
                                {"$set": {"is_auto_or_manual": bulb.is_auto_or_manual, 
                                            "is_it_open": bulb.is_it_open}})
        return {"Data has been collected."}

#Send data to front update status
@app.get("/front/get_status")
def send_bulb_to_front():
    r = get_all_bulb_status()
    return {"results":r}

# Hard
#hardware get data from back
@app.get("/hard/get_status")
def get_status():
    res = get_all_bulb_status()
    return res

#Hard send status to back
@app.post("/hard/send_status")
def reciecve_status(bulb: Bulb):
    bulbs = bulb_collecton.find({"bulb_id":bulb.bulb_id}, {"_id": False})
    if bulbs:
        bulb_collecton.update_one({"bulb_id": bulb.bulb_id}, 
                                {"$set": {"is_auto_or_manual": bulb.is_auto_or_manual, 
                                            "is_it_open": bulb.is_it_open}})
        return {"Data has been updated."}



    
     




