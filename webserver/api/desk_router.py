
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from . import desk_gpio


class MotorInput(BaseModel):
    speed: Optional[int] = Field(default=None, ge=0, le=100, description="values must be between 0 and 100")
    frequency: Optional[int] = None
    transition: Optional[float] = Field(default=None, ge=0, le=30, description="value must be between 1 and 30")


desk_router = APIRouter(prefix="/api/desk", tags=["desk"])


def _input_to_config(motor_input: MotorInput) -> dict:
    speed = motor_input.speed / 100 if motor_input.speed else None
    frequency = motor_input.frequency
    transition = motor_input.transition
    return {'speed': speed, 'frequency': frequency, 'transition_time': transition}


@desk_router.post("/up")
def move_desk_up(motor_input: MotorInput):
    desk_gpio.desk.motor.config(**_input_to_config(motor_input))
    desk_gpio.desk.motor.forward()
    return {"ok": True}


@desk_router.post("/stop")
def stop_desk(motor_input: MotorInput):
    desk_gpio.desk.motor.config(**_input_to_config(motor_input))
    desk_gpio.desk.motor.stop()
    return {"ok": True}


@desk_router.post("/down")
def move_desk_down(motor_input: MotorInput):
    desk_gpio.desk.motor.config(**_input_to_config(motor_input))
    desk_gpio.desk.motor.backward()
    return {"ok": True}


@desk_router.post("/motor")
def desk_motor(motor_input: MotorInput):
    # desk_gpio.desk.motor.config(**_input_to_config(motor_input))
    # desk_gpio.desk.motor.update()
    if motor_input.frequency is not None:
        desk_gpio.desk.motor.enable_device.frequency = motor_input.frequency
    if motor_input.speed is not None:
        desk_gpio.desk.motor.value = motor_input.speed / 100

    return {"ok": True}
