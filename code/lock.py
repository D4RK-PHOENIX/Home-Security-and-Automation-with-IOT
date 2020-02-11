import time
import RPi.GPIO as GPIO
from keypad import keypad
 
GPIO.setwarnings(False)
 
if __name__ == '__main__':
    kp = keypad(columnCount = 4)
    digit = None
    while True:
        seq = []
        for i in range(4):
            digit = None
            while digit == None:
                digit = kp.getKey()
            seq.append(digit)
            print(seq)
            time.sleep(0.4)
 
        # Check digit code
        if seq == [1, 2, 3, '#']:
            print "Code accepted"
        else:
            print("Code rejected")
