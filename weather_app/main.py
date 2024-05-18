from fastapi import FastAPI, Header, HTTPException
from decouple import config

from weather import Weather

app = FastAPI()


@app.get("/")
async def index():
    return {"Message": "Ok"}


@app.get("/{town_name}")
async def get_weather(town_name: str, token: str = Header(None)):
    if token == "borko":
        weather = Weather(config('name_pos_token'), config('WEATHER_TOKEN'))
        return {"weather": weather.weather_parse(town_name)}
    return HTTPException(detail="Not valid", status_code=401)