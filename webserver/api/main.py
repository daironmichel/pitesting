
from typing import Optional
from fastapi import FastAPI
from gpiozero import LED

app = FastAPI()
led = LED(4)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/api/ledon")
def api_ledon():
    led.on()


@app.post("/api/ledoff")
def api_ledoff():
    led.off()
