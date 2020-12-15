from typing import Optional

from gpiozero import Button, PhaseEnableMotor


class Desk:
    def __init__(self):
        self.up_button: Button = Button(23)
        self.down_button: Button = Button(24)
        self.motor: PhaseEnableMotor = PhaseEnableMotor(6, 13)  # pins(dir, pwm)

        self.up_button.when_activated = self.up_pressed
        self.up_button.when_deactivated = self.up_or_down_released
        self.down_button.when_activated = self.down_pressed
        self.down_button.when_deactivated = self.up_or_down_released

    def up_pressed(self):
        print("forward")
        self.motor.forward()

    def up_or_down_released(self):
        print("stop")
        self.motor.stop()

    def down_pressed(self):
        print("backward")
        self.motor.backward()


desk: Optional[Desk] = None


def init():
    print("initializing desk")
    global desk
    desk = Desk()
