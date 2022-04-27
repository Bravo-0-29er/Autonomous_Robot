import RPi.GPIO as GPIO
import time
from multiprocessing import Process,Pipe

def getDistance_right(child_conn):
    GPIO.setmode (GPIO.BCM)
    GPIO.setwarnings(False)

    ECHO = 6
    TRIG = 5

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    print("Distance Measured In Progress")
    try:
        GPIO.output(TRIG,False)
        while True:
            time.sleep(1)
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO)==0:
                pulse_start = time.time()

            while GPIO.input(ECHO)==1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            print("Distance Right: ",distance," cm")
            child_conn.send(distance)
    except KeyboardInterrupt:
        GPIO.cleanup()

def getDistance_left(child_conn):
    GPIO.setmode (GPIO.BCM)
    GPIO.setwarnings(False)

    ECHO = 24
    TRIG = 23

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    print("Distance Measured In Progress")
    try:
        GPIO.output(TRIG,False)
        while True:
            time.sleep(1)
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO)==0:
                pulse_start = time.time()

            while GPIO.input(ECHO)==1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            print("Distance Left: ",distance," cm")
            child_conn.send(distance)
    except KeyboardInterrupt:
        GPIO.cleanup()
