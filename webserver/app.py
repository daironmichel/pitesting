import os
from fastapi import FastAPI, Request
from .api import desk_gpio
from .api.desk_router import desk_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()
app.mount("/static", StaticFiles(directory=f"{BASE_DIR}/webserver/static"), name="static")
templates = Jinja2Templates(directory=f"{BASE_DIR}/webserver/templates")
app.include_router(desk_router)


@app.on_event("startup")
async def startup_event():
    desk_gpio.init()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
