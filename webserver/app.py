from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse

from .api import desk_gpio
from .api.desk_router import desk_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from webserver.settings import BASE_DIR, DEBUG

app = FastAPI()
app.mount("/dashboard", StaticFiles(directory=f"{BASE_DIR}/frontend/build"), name="root")
templates = Jinja2Templates(directory=f"{BASE_DIR}/frontend/build")
app.include_router(desk_router)


@app.on_event("startup")
async def startup_event():
    if DEBUG:
        return

    print("INFO: initializing GPIO")
    desk_gpio.init()


@app.get("/", response_class=HTMLResponse)
async def root():
    # return templates.TemplateResponse("index.html", {"request": request})
    return RedirectResponse("/dashboard/index.html")
