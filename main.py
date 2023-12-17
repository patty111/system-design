import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from api.url import router as url_router
from api.user import router as user_router
from config import config

app = FastAPI()
app.include_router(url_router)
app.include_router(user_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# TODO: Create db at startup if not exists
@app.on_event("startup")
def startup_event():
    pass

@app.get("/", response_class=HTMLResponse)
async def root():
    with open('static/index.html', 'r') as f:
        return HTMLResponse(content=str(f.read()))

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", host=config.host, port=int(config.port), reload=True, log_level="info")
    