#!/usr/bin/python

from multiprocessing import Process,Queue,Pipe
import time
from Sensor import getDistance_right,getDistance_left
from PCA9685 import PCA9685
import time

Dir = [
    'forward',
    'backward',
]
pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)

class MotorDriver():
    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

    def MotorRun(self, motor, index, speed):
        if speed > 100:
            return
        if(motor == 0):
            pwm.setDutycycle(self.PWMA, speed)
            if(index == Dir[0]):
                #print ("1")
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                #print ("2")
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:
            pwm.setDutycycle(self.PWMB, speed)
            if(index == Dir[0]):
                #print ("3")
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                #print ("4")
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

    def MotorStop(self, motor):
        if (motor == 0):
            pwm.setDutycycle(self.PWMA, 0)
        else:
            pwm.setDutycycle(self.PWMB, 0)
            
def halt():
    Motor.MotorRun(0, 'forward', 75)
    Motor.MotorRun(1, 'forward', 75)
    time.sleep(0.25)
    Motor.MotorRun(0, 'forward', 30)
    Motor.MotorRun(1, 'forward', 30)
    time.sleep(0.25)
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    
def move():
    Motor.MotorRun(0, 'forward', 100)
    Motor.MotorRun(1, 'forward', 100)

print(" press Ctrl+c to stop program ")
try:            
    Motor = MotorDriver()

    #print("Main File")
    #print("Calling Sensor.py")
    if __name__ == '__main__':
        parent_conn_left,child_conn_left = Pipe()
        p_left = Process(target=getDistance_left, args=(child_conn_left,))
        p_left.start()
        parent_conn_right,child_conn_right = Pipe()
        p_right = Process(target=getDistance_right, args=(child_conn_right,))
        p_right.start()
        Running = False;
        while True:
            distance_left = parent_conn_left.recv()
            distance_right = parent_conn_right.recv()
            if distance_left < 25.0 or distance_right < 25.0:
                print("Stop the cart")
                if Running:
                    halt()
                    Running = False
            else:
                print("Continue")
                if not Running:
                    move()
                    Running = True
            time.sleep(1)
except KeyboardInterrupt:
    Motor.MotorStop(0)
    Motor.MotorStop(1)
