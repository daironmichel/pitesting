import math
from itertools import repeat, cycle, chain
from typing import Optional

from gpiozero import Button, PhaseEnableMotor, PWMOutputDevice, OutputDeviceBadValue, GPIOPinMissing, \
    DigitalOutputDevice
from gpiozero.threads import GPIOThread
from pigpio import pi


class PWMTransitionOutputDevice(PWMOutputDevice):

    def _blink_device(
            self, on_time, off_time, fade_in_time, fade_out_time, n, fps=25, min_value=0, max_value=1):
        if not 0 <= min_value <= 1:
            raise OutputDeviceBadValue("min_value must be between 0 and 1")
        if not 0 <= max_value <= 1:
            raise OutputDeviceBadValue("max_value must be between 0 and 1")
        if not min_value <= max_value:
            raise OutputDeviceBadValue("min_value must be less than max_value")
        amount_to_move = max_value - min_value
        sequence = []
        if fade_in_time > 0:
            sequence += [
                (min_value + (i * (amount_to_move / fps) / fade_in_time), 1 / fps)
                for i in range(int(fps * fade_in_time))
                ]
        if on_time is not None:
            sequence.append((max_value, on_time))
        if fade_out_time > 0:
            sequence += [
                (max_value - (i * (amount_to_move / fps) / fade_out_time), 1 / fps)
                for i in range(int(fps * fade_out_time))
                ]
        if off_time is not None:
            sequence.append((min_value, off_time))
        sequence = (
                cycle(sequence) if n is None else
                chain.from_iterable(repeat(sequence, n))
                )
        for value, delay in sequence:
            self._write(value)
            if self._blink_thread.stopping.wait(delay):
                break

    def blink(
            self, on_time=1, off_time=1, fade_in_time=0, fade_out_time=0, n=None, background=True, fps=25,
            min_value=0, max_value=1):
        if not 0 <= min_value <= 1:
            raise OutputDeviceBadValue("min_value must be between 0 and 1")
        if not 0 <= max_value <= 1:
            raise OutputDeviceBadValue("max_value must be between 0 and 1")
        if not min_value <= max_value:
            raise OutputDeviceBadValue("min_value must be less than max_value")
        try:
            self._stop_blink()
        except RuntimeError as e:
            if "cannot join thread before it is started" not in str(e):
                raise e

        self._blink_thread = GPIOThread(
            target=self._blink_device,
            args=(on_time, off_time, fade_in_time, fade_out_time, n, fps, min_value, max_value)
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

        self.speed = 1
        self.frequency = 3000
        self.transition_time = 1

    def config(self, speed=None, frequency=None, transition_time=None):
        if speed and 0 <= speed <= 1:
            self.speed = speed
        if frequency is not None:
            self.frequency = frequency
        if transition_time is not None:
            self.transition_time = transition_time

    def forward(self, speed=None, speed_up_time=None):
        target_frequency = self.frequency
        target_transition_time = speed_up_time if speed_up_time is not None else self.transition_time
        target_speed = speed if speed is not None else self.speed

        if isinstance(self.enable_device, DigitalOutputDevice):
            if speed not in (0, 1):
                raise ValueError(
                    'forward speed must be 0 or 1 with non-PWM Motors')

        self.enable_device.off()
        self.phase_device.off()

        if isinstance(self.enable_device, PWMOutputDevice):
            self.enable_device.frequency = target_frequency

        self.enable_device.blink(
            on_time=0, off_time=None, fade_in_time=target_transition_time, max_value=target_speed, n=1)

    def backward(self, speed=None, speed_up_time=None):
        target_frequency = self.frequency
        target_transition_time = speed_up_time if speed_up_time is not None else self.transition_time
        target_speed = speed if speed is not None else self.speed

        if isinstance(self.enable_device, DigitalOutputDevice):
            if speed not in (0, 1):
                raise ValueError(
                    'backward speed must be 0 or 1 with non-PWM Motors')
        self.enable_device.off()
        self.phase_device.on()

        if isinstance(self.enable_device, PWMOutputDevice):
            self.enable_device.frequency = target_frequency

        self.enable_device.blink(
            on_time=0, off_time=None, fade_in_time=target_transition_time, max_value=target_speed, n=1)

    def stop(self, speed_down_time=None):
        """
        Stop the motor.
        """
        self.update(speed=0, transition_time=speed_down_time)

    def update(self, speed=None, frequency=None, transition_time=None):
        target_frequency = frequency if frequency is not None else self.frequency
        target_transition_time = transition_time if transition_time is not None else self.transition_time
        target_speed = speed if speed is not None else self.speed
        current_speed = math.fabs(self.value)
        if isinstance(self.enable_device, PWMOutputDevice):
            self.enable_device.frequency = target_frequency


        if current_speed < target_speed:
            self.enable_device.blink(
                on_time=0, off_time=None, fade_in_time=target_transition_time,
                min_value=current_speed, max_value=target_speed, n=1)
        else:
            self.enable_device.blink(
                on_time=None, off_time=0, fade_out_time=target_transition_time,
                min_value=target_speed, max_value=current_speed, n=1)


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


desk: Optional[Desk] = None


def init():
    # print("initializing desk")
    global desk
    desk = Desk()
