import RPi.GPIO as GPIO
from time import sleep

def restart():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)

    # On
    print("turn on")
    GPIO.output(11, GPIO.HIGH)
    # Wait a bit
    sleep(1)
    print("turn off")
    # Off
    GPIO.output(11, GPIO.LOW)
    GPIO.cleanup()

def start():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)

    # On
    print("turn on")
    GPIO.output(12, GPIO.HIGH)
    # Wait a bit
    sleep(1)
    print("turn off")
    # Off
    GPIO.output(12, GPIO.LOW)
    GPIO.cleanup()

if __name__ == "__main__":
    restart()