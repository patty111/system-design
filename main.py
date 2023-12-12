import hashlib
import requests
import os
import uvicorn
import gunicorn
from fastapi import FastAPI, Form, status, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, MetaData, Table, select
from api.url import router as url_router
from config import config

# 8 length short url, [0-9a-zA-Z]
base62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

app = FastAPI()
app.include_router(url_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup_event():
    pass

@app.get("/", response_class=HTMLResponse)
async def root():
    with open('static/index.html', 'r') as f:
        return HTMLResponse(content=str(f.read()))

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", host=config.host, port=int(config.port), reload=True, log_level="info")
    