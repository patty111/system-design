import hashlib
import atexit
import requests
import sqlite3
import os
from fastapi import FastAPI, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse

# database operations
if not os.path.exists('shorturl.db'):
    conn = sqlite3.connect('shorturl.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE urls
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_url TEXT NOT NULL,
                long_url TEXT NOT NULL)''')
    conn.commit()
else:
    conn = sqlite3.connect('shorturl.db')

c = conn.cursor()
# 這個用法記起來     
atexit.register(conn.close)


# 8 length short url, [0-9a-zA-Z]
base62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
app = FastAPI()

class urldata():
    def __init__(self, long_url: str):
        self.long_url = long_url
        self.short_url = converter(long_url)   # PRIMARY KEY

def converter(long_url: str):
    hash_res = hashlib.sha256(long_url.encode('utf-8')).hexdigest()
    num = int(hash_res, 16)

    result_str = ""
    while num:
        result_str = f"{base62[num % 62]}{result_str}"
        num = num // 62
    return result_str[:8]

def check_valid_link(link: str):
    if requests.get(link).status_code == 200:
        return True
    return False


@app.get("/")
async def root():
    return RedirectResponse("/main")

@app.get("/main")
async def main():
    return {"message": "Hello World"}

@app.post("/main")
async def create(long_url: str = Form(...)):
    if check_valid_link(long_url) == False:
        return {"message": "Invalid URL"}

    c.execute("SELECT * FROM urls WHERE long_url = ?", (long_url,))
    result = c.fetchone()

    if result:
        return {"shortened url": f"http://127.0.0.1:8000/{result[1]}"}
    else:
        tmp = urldata(long_url)
        c.execute("INSERT INTO urls (long_url, short_url) VALUES (?, ?)", (long_url, tmp.short_url))
        conn.commit()
        return {"shortened url": f"http://127.0.0.1:8000/{tmp.short_url}"}



@app.get("/{shortened_url}")
async def redirect(shortened_url: str = None):
    if shortened_url:
        c.execute("SELECT * FROM urls WHERE short_url = ?", (shortened_url,))
        result = c.fetchone()

        if result:
            return RedirectResponse(url=result[2], status_code=status.HTTP_303_SEE_OTHER)
        return {"message": "Short URL not found"}
    else:
        return RedirectResponse(url="/main")