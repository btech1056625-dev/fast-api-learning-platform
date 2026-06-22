from fastapi import FastAPI 
from pydantic import BaseModel
from typing import List


app  =  FastAPI()

class info(BaseModel):
    id : int 
    Name : str
    marks : int

infos : List[info] = []

@app.get("/")
def welcome():
    return { "Welcome !!!" }

@app.get("/info/{info_id}")
def read_info(info_id : int , read_info : info):
    for i in enumerate(infos) :
        if i.id == info_id :
            return i
    return "info not found"

@app.delete("/info/{info_id}")
def delete_info(info_id : int):
    for i in enumerate(infos) :
        if info.id == info_id :
            infos.pop(i)
