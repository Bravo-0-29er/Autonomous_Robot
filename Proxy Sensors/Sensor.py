import RPi.GPIO as GPIO
import time
from multiprocessing import Process, Pipe

# https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

def getDistance(child_conn):
    
    # define constants
    TRIG = 23 # pin that triggers the sensor
    ECHO = 24 # pin that reads signal return from the sensor

    # print("Distance Measured In Progress")

    # configure GPIO pins
    GPIO.setmode(GPIO.BCM) # configure pin numbering
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, False)

    while True:

        time.sleep(1)
        
        # create sensor pulse
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # get time stamps for start and end of pulse
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        # calculate distance based on pulse duration
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print("Distance: " + distance + " cm")
        child_conn.send(distance)

GPIO.cleanup() 
