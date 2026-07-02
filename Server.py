from operator import truediv

from fastapi import FastAPI
import random
import httpx
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import encrypt
import decrypt

class Town(BaseModel):
    latitude: float
    longitude: float

class CeaserReq(BaseModel):
    text: str
    shift: int

class CeaserResp(BaseModel):
    text: str
    req: CeaserReq

class VigenereReq(BaseModel):
    text: str
    key: str

class VigenereResp(BaseModel):
    text: str
    req: VigenereReq

class XorReq(BaseModel):
    text: str
    key: str

class XorResp(BaseModel):
    text: str
    req: XorReq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
GITHUB_URL = "https://api.github.com/user/repos"
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@app.get("/")
async def root():
    return {"message": "Server says hello"}


@app.get("/isAleksGay")
async def is_aleks_gay():
    rnd = random.randint(1, 10)

    if rnd < 9:
        return True
    else:
        return False


@app.post("/weather")
async def get_weather(town : Town):
    params = {
        "latitude": town.latitude,
        "longitude": town.longitude,
        "current": "temperature_2m,apparent_temperature,precipitation,wind_speed_10m"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_URL, params=params)
        data = response.json()

    return {
        "temperature": data["current"]["temperature_2m"],
        "apparent_temperature": data["current"]["apparent_temperature"],
        "wind": data["current"]["wind_speed_10m"],
        "precipitation": data["current"]["precipitation"]
    }


@app.get("/repos")
async def get_repos():
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    params = {
        "sort": "updated",
        "per_page": 100
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GITHUB_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

    return [
        {
            "name": repo["name"],
            "description": repo["description"],
            "url": repo["html_url"],
            "language": repo["language"],
            "updated_at": repo["updated_at"]
        }
        for repo in data
    ]

@app.post("/caeser/decrypt")
async def handle_ceaser_decrypt(req: CeaserReq):

    result = decrypt.ceaser(req.text, req.shift)

    resp = CeaserResp(
        text=result,
        req=req
    )

    return resp

@app.post("/vigenere/decrypt")
async def handle_vigenere_decrypt(req: VigenereReq):
    result = decrypt.vigenere(req.text, req.key)

    resp = VigenereResp(
        text=result,
        req=req
    )

    return resp

@app.post("/caeser/encrypt")
async def handle_ceaser_encrypt(req: CeaserReq):
    result = encrypt.ceaser(req.text, req.shift)

    resp = CeaserResp(
        text=result,
        req=req
    )

    return resp

@app.post("/vigenere/encrypt")
async def handle_vigenere_encrypt(req: VigenereReq):
    result = encrypt.vigenere(req.text, req.key)

    resp = VigenereResp(
        text=result,
        req=req
    )

    return resp

@app.post("/xor/encrypt")
async def handle_xor_encrypt(req: XorReq):
    result = encrypt.xor(req.text, req.key)

    resp = XorResp(
        text=result,
        req=req
    )

    return resp