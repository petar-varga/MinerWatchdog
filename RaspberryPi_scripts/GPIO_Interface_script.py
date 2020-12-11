import RPi.GPIO as GPIO
from time import sleep
from utils import (
    db_insert_id, db_read, db_write, db_write_executemany
)


def restart(raspberry_pin):
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(raspberry_pin, GPIO.OUT)

    # On
    print(f"turn ON pin {raspberry_pin}")
    GPIO.output(raspberry_pin, GPIO.HIGH)
    # Wait a bit
    sleep(1)
    print(f"turn OFF pin {raspberry_pin}")
    # Off
    GPIO.output(raspberry_pin, GPIO.LOW)
    GPIO.cleanup()

def start(raspberry_pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(raspberry_pin, GPIO.OUT)

    # On
    print(f"turn ON pin {raspberry_pin}")
    GPIO.output(raspberry_pin, GPIO.HIGH)
    # Wait a bit
    sleep(1)
    print(f"turn OFF pin {raspberry_pin}")
    # Off
    GPIO.output(raspberry_pin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == "__main__":
    restart("DESKTOP-E9B2NU2")