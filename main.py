import dill
import pandas as pd
import json

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
with open('model/Sber_AP_pipe.pkl', 'rb') as file:
    model = dill.load(file)


class Form(BaseModel):
    session_id: str
    client_id: str
    visit_date: str
    visit_time: str
    visit_number: int
    utm_source: str
    utm_medium: str
    utm_campaign: str
    utm_adcontent: str
    utm_keyword: str
    device_category: str
    device_os: str
    device_brand: str
    device_model: str
    device_screen_resolution: str
    device_browser: str
    geo_country: str
    geo_city: str


class Prediction(BaseModel):
    Client_ID: str
    Session_ID: str
    Result: int


@app.get("/status")
def status():
    return "I'm OK"


@app.get("/version")
def version():
    return model['metadata']


@app.post("/predict", response_model=Prediction)
def prediction(form: Form):
    df = pd.DataFrame.from_dict([form.dict()])
    y = model['model'].predict(df)

    return {
        'Client_ID': form.client_id,
        'Session_ID': form.session_id,
        'Result': y[0]
    }
