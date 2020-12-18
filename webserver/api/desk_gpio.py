from itertools import repeat, cycle, chain
from typing import Optional

from gpiozero import Button, PhaseEnableMotor, PWMOutputDevice, OutputDeviceBadValue, GPIOPinMissing, \
    DigitalOutputDevice
from gpiozero.threads import GPIOThread
from pigpio import pi


class PWMTransitionOutputDevice(PWMOutputDevice):

    def _blink_device(
            self, on_time, off_time, fade_in_time, fade_out_time, n, fps=25, max_value=1):
        if not 0 <= max_value <= 1:
            raise OutputDeviceBadValue("max_value must be between 0 and 1")
        sequence = []
        if fade_in_time > 0:
            sequence += [
                (i * (max_value / fps) / fade_in_time, 1 / fps)
                for i in range(int(fps * fade_in_time))
                ]
        if on_time is not None:
            sequence.append((max_value, on_time))
        if fade_out_time > 0:
            sequence += [
                (max_value - (i * (max_value / fps) / fade_out_time), 1 / fps)
                for i in range(int(fps * fade_out_time))
                ]
        if off_time is not None:
            sequence.append((0, off_time))
        sequence = (
                cycle(sequence) if n is None else
                chain.from_iterable(repeat(sequence, n))
                )
        for value, delay in sequence:
            self._write(value)
            if self._blink_thread.stopping.wait(delay):
                break

    def blink(
            self, on_time=1, off_time=1, fade_in_time=0, fade_out_time=0, n=None, background=True, fps=25, max_value=1):
        if not 0 <= max_value <= 1:
            raise OutputDeviceBadValue("max_value must be between 0 and 1")
        self._stop_blink()
        self._blink_thread = GPIOThread(
            target=self._blink_device,
            args=(on_time, off_time, fade_in_time, fade_out_time, n, fps, max_value)
        )
        self._blink_thread.start()
        if not background:
            self._blink_thread.join()
            self._blink_thread = None


class DeskMotor(PhaseEnableMotor):

    def __init__(self, phase=None, enable=None, pwm=True, pin_factory=None):
        if not all([phase, enable]):
            raise GPIOPinMissing('phase and enable pins must be provided')
        PinClass = PWMTransitionOutputDevice if pwm else DigitalOutputDevice
        super(PhaseEnableMotor, self).__init__(
            phase_device=DigitalOutputDevice(phase, pin_factory=pin_factory),
            enable_device=PinClass(enable, pin_factory=pin_factory),
            _order=('phase_device', 'enable_device'),
            pin_factory=pin_factory
        )

    def forward(self, speed=1, speed_up_time=1):
        if isinstance(self.enable_device, DigitalOutputDevice):
            if speed not in (0, 1):
                raise ValueError(
                    'forward speed must be 0 or 1 with non-PWM Motors')
        self.enable_device.off()
        self.phase_device.off()
        self.enable_device.blink(
            on_time=None, off_time=None, fade_in_time=speed_up_time, max_value=speed, n=1)

    def backward(self, speed=1, speed_up_time=1):
        if isinstance(self.enable_device, DigitalOutputDevice):
            if speed not in (0, 1):
                raise ValueError(
                    'backward speed must be 0 or 1 with non-PWM Motors')
        self.enable_device.off()
        self.phase_device.on()
        self.enable_device.blink(
            on_time=None, off_time=None, fade_in_time=speed_up_time, max_value=speed, n=1)
        
    def stop(self, speed_down_time=1):
        """
        Stop the motor.
        """
        self.enable_device.blink(
            on_time=None, off_time=None, fade_out_time=speed_down_time, max_value=self.value, n=1)


class Desk:
    PHASE_PIN = 6
    ENABLE_PIN = 12

    def __init__(self):
        self.pi = pi()
        self.up_button: Button = Button(23)
        self.down_button: Button = Button(24)
        self.motor: DeskMotor = DeskMotor(6, 12)  # pins(dir, pwm)
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
