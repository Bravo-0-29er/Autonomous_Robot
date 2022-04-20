#!/usr/bin/python

from multiprocessing import Process,Queue,Pipe
import time
from Sensor import getDistance
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
    Motor.MotorRun(0, 'forward', 50)
    Motor.MotorRun(1, 'forward', 50)
    time.sleep(0.5)
    Motor.MotorRun(0, 'forward', 25)
    Motor.MotorRun(1, 'forward', 25)
    time.sleep(0.5)
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    
def move():
    Motor.MotorRun(0, 'forward', 75)
    Motor.MotorRun(1, 'forward', 75)
            
Motor = MotorDriver()

print("Main File")
print("Calling Sensor.py")
if __name__ == '__main__':
    parent_conn,child_conn = Pipe()
    p = Process(target=getDistance, args=(child_conn,))
    p.start()
    Running = True;
    while True:
        distance = parent_conn.recv()
        if distance < 50.0:
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

Motor.MotorStop(0)
Motor.MotorStop(1)