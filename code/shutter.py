#!/usr/bin/env python
import RPi.GPIO as GPIO
import SimpleMFRC522
import time
GPIO.setmode(GPIO.BCM)
servo=5     #Pin number29
#For RFID pin numbers are 24,23,19,21,GND,22,Power resp...no pin for RQ.
GPIO.setup(servo,GPIO.OUT)
GPIO.setwarnings(False)
p=GPIO.PWM(5,50) #50hz
#p.start(5.5) #neutral pos
reader= SimpleMFRC522.SimpleMFRC522()
p.start(11) #neutral pos
while True:
    print("Place the tag")
    id,text = reader.read()
    print(id)
    print(text)
    if id==712752615109:
        print('Door opened')
        p.ChangeDutyCycle(5)  #180
        time.sleep(5)
        p.ChangeDutyCycle(11)  #0
        time.sleep(1)
        
    else:
        print("Wrong tag, cannot open this door!")
GPIO.cleanup()
