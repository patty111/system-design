import hashlib
import requests
import os
import uvicorn
from fastapi import FastAPI, Form, status, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, MetaData, Table, select
from api.url import router as url_router
from config import config

# 8 length short url, [0-9a-zA-Z]
base62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
app = FastAPI()

app.include_router(url_router)

# class urldata():
#     def __init__(self, long_url: str):
#         self.long_url = long_url
#         self.short_url = converter(long_url)   # PRIMARY KEY

# def converter(long_url: str):
#     hash_res = hashlib.md5(long_url.encode('utf-8')).hexdigest()
#     num = int(hash_res, 16)

#     result_str = ""
#     while num:
#         result_str = f"{base62[num % 62]}{result_str}"
#         num = num // 62
#     return result_str[:8]

# def check_valid_link(link: str):
#     try:
#         if requests.get(link).status_code == 200:
#             return True
#         return False
#     except:
#         return False



# @app.get("/", response_class=HTMLResponse)
# async def root():
#     return RedirectResponse("/main")

# @app.get("/main")
# async def main():
#     with open('static/index.html', 'r') as f:
#         return HTMLResponse(content=str(f.read()))

# @app.put("/main")
# async def create(long_url: str = Form(...)):
#     if check_valid_link(long_url) == False:
#         return "Invalid URL"

#     c.execute("SELECT * FROM urls WHERE long_url = ?", (long_url,))
#     result = c.fetchone()

#     if result:
#         return f"https://veryshort.onrender.com/{result[1]}"
#     else:
#         tmp = urldata(long_url)
#         c.execute("INSERT INTO urls (long_url, short_url) VALUES (?, ?)", (long_url, tmp.short_url))
#         conn.commit()
#         return f"https://veryshort.onrender.com/{tmp.short_url}"
    
# # @app.get("/{shortened_url}")
# # async def redirect(shortened_url: str = None):
# #     if shortened_url:
# #         c.execute("SELECT * FROM urls WHERE short_url = ?", (shortened_url,))
# #         result = c.fetchone()

# #         if result:  
# #             print(result)
# #             c.execute("UPDATE urls SET request_count = request_count + 1 WHERE short_url = ?", (result[1],))
# #             conn.commit()
# #             return RedirectResponse(url=result[2], status_code=status.HTTP_303_SEE_OTHER)
# #         return {"message": "Short URL not found"}
# #     else:
# #         return RedirectResponse(url="/main")

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", host=config.host, port=int(config.port), reload=True, log_level="info")
    