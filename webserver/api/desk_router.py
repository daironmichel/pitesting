
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from . import desk_gpio

desk_router = APIRouter(prefix="/api/desk", tags=["desk"])


@desk_router.post("/up")
def move_desk_up():
    desk_gpio.desk.motor.forward()
    return {"ok": True}


@desk_router.post("/stop")
def stop_desk():
    desk_gpio.desk.motor.stop()
    return {"ok": True}


@desk_router.post("/down")
def move_desk_down():
    desk_gpio.desk.motor.backward()
    return {"ok": True}


class MotorInput(BaseModel):
    speed: Optional[int]
    frequency: Optional[int]


@desk_router.post("/motor")
def desk_motor(motor_input: MotorInput):
    if motor_input.frequency is not None:
        desk_gpio.desk.motor.enable_device.frequency = motor_input.frequency
    if motor_input.speed is not None:
        # if desk_gpio.desk.motor.value >= 0:
        #     desk_gpio.desk.motor.forward(motor_input.speed / 100)
        # else:
        #     desk_gpio.desk.motor.backward(motor_input.speed / 100)
        desk_gpio.desk.motor.value = motor_input.speed / 100

    return {"ok": True}


# @desk_router.get("/")
# def motor_forward():
#     desk_gpio.desk.motor.forward()
#     return {"Hello": "World"}
#
#
# @desk_router.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
#
#
# @desk_router.post("/ledon")
# def api_ledon():
#     led.on()
#
#
# @desk_router.post("/ledoff")
# def api_ledoff():
#     led.off()
