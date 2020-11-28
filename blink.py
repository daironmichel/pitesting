import RPi.GPIO as GPIO
import time

LED = 4  # pin connected to the LED
ON = True  # could also be 1 or GPIO.HIGH
OFF = False  # could also be 0 or GPIO.LOW

def setup():
    print('setting things up...')
    # GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED, GPIO.OUT)

def switch_led(value):
    print(f'switching LED {"ON" if value else "OFF"}')
    GPIO.output(LED, value)

def blink():
    print('blinking...')
    switch_led(OFF)
    for _ in range(12):
        switch_led(ON)
        time.sleep(0.25)
        switch_led(OFF)
        time.sleep(0.25)

def end():
    print('cleaning...')
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    option = '0'
    while option != '3':
        print('')
        print('Ready')
        print('0: LED OFF')
        print('1: LED ON')
        print('2: Blink')
        print('3: Exit')
        option = input('Enter a value from 0 to 3: ')
        if option not in ('0','1','2','3'):
            print('Invalid option, try again.')
            continue
        if option == '0':
            switch_led(OFF)
            continue
        elif option == '1':
            switch_led(ON)
            continue
        elif option == '2':
            blink()
            continue
        else:
            print('Exit')
    end()
