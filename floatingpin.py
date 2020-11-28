import RPi.GPIO as gpio
import time
import sys

BUTTON_PIN = 4

if __name__ == '__main__':
    gpio.setmode(gpio.BCM)
    gpio.setup(BUTTON_PIN, gpio.IN, pull_up_down=gpio.PUD_UP)

    try:
        while True:
            data = gpio.input(BUTTON_PIN)
            if data:
                print(f'HIGH {data}')
            else:
                print(f'LOW {data}')
            time.sleep(0.5)
    except:
       print("Unexpected error:", sys.exc_info()[0])
       gpio.cleanup()
