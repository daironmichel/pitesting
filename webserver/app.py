from fastapi import FastAPI, Request
from .api import desk_gpio
from .api.desk_router import desk_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from webserver.settings import BASE_DIR, DEBUG

app = FastAPI()
app.mount("/static", StaticFiles(directory=f"{BASE_DIR}/webserver/static"), name="static")
templates = Jinja2Templates(directory=f"{BASE_DIR}/webserver/templates")
app.include_router(desk_router)


@app.on_event("startup")
async def startup_event():
    if DEBUG:
        return

    print("init gpio")
    desk_gpio.init()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
