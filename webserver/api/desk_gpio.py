from typing import Optional

from pigpio import pi
from gpiozero import Button, PhaseEnableMotor


class Desk:
    PHASE_PIN = 6
    ENABLE_PIN = 12

    def __init__(self):
        self.pi = pi()
        self.up_button: Button = Button(23)
        self.down_button: Button = Button(24)
        self.motor: PhaseEnableMotor = PhaseEnableMotor(6, 12)  # pins(dir, pwm)
        self.motor.enable_device.frequency = 3000

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

    def set_motor_speed(self, value: float):
        if not self.motor.is_active:
            return
        if not 0 <= value <= 1:
            return
        pwm_value = int(255 * value)
        print(f"setting pwm: {pwm_value}")
        self.pi.set_PWM_dutycycle(self.ENABLE_PIN, pwm_value)


desk: Optional[Desk] = None


def init():
    # print("initializing desk")
    global desk
    desk = Desk()
