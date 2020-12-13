
from typing import Optional
from fastapi import APIRouter
from gpiozero import LED

desk_router = APIRouter(prefix="/api/desk", tags=["desk"])

led = LED(4)


@desk_router.get("/")
def read_root():
    return {"Hello": "World"}


@desk_router.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@desk_router.post("/ledon")
def api_ledon():
    led.on()


@desk_router.post("/ledoff")
def api_ledoff():
    led.off()
