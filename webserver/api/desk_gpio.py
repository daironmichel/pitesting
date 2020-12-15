from typing import Optional

from gpiozero import Button, PhaseEnableMotor


class Desk:
    def __init__(self):
        self.up_button: Button = Button(23)
        self.down_button: Button = Button(24)
        self.motor: PhaseEnableMotor = PhaseEnableMotor(6, 12)  # pins(dir, pwm)

        self.up_button.when_activated = self.up_pressed
        self.up_button.when_deactivated = self.up_or_down_released
        self.down_button.when_activated = self.down_pressed
        self.down_button.when_deactivated = self.up_or_down_released

    def up_pressed(self):
        # print("forward")
        self.motor.forward()
        # print(f"motor: {self.motor.__dict__}")

    def up_or_down_released(self):
        # print("stop")
        self.motor.stop()

    def down_pressed(self):
        # print("backward")
        self.motor.backward()
        # print(f"motor: {self.motor.__dict__}")


desk: Optional[Desk] = None


def init():
    # print("initializing desk")
    global desk
    desk = Desk()
