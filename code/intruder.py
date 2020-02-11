#Home Automation Using Raspberry Pi
#Intruder Detection System
import RPi.GPIO as GPIO
from keypad import keypad
from picamera import PiCamera
import time, datetime
import MySQLdb
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
pins= [33,35,37,7]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,0)
seq= [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
#ROW_PINS= [36,16,18,38]
#COL_PINS= [11,13,15,10]
cam=PiCamera()
dateString = '%Y-%m-%d %H-%M-%S'
led=31
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led,GPIO.OUT)      
time.sleep(1) 
if __name__ == '__main__':
    kp = keypad(columnCount = 4)
    digit = None
    while True:
        code = []
        for i in range(4):
            digit = None
            while digit == None:
                digit = kp.getKey()
            code.append(digit)
            print(code)
            time.sleep(0.4)
        if code == [1, 2, 3, '#']:
            print "Code accepted"
            for i in range(620):
                for halfstep in range(8):
                    for pin in range (4):
                        GPIO.output(pins[pin],seq[halfstep][pin])
                    time.sleep(0.001)
            time.sleep(2)
            for i in range(620):
                for halfstep in reversed(xrange(8)):
                    for pin in reversed(xrange(4)):
                        GPIO.output(pins[pin],seq[halfstep][pin])
                    time.sleep(0.001)
            z= datetime.datetime.now().strftime(dateString)#STORING DATE AND TIME IN A VARIABLE
            db=MySQLdb.connect("localhost","root","xaviers123","datalog")
            curs=db.cursor()
            with db:
                curs.execute("""INSERT into generallog values (%s)""",(z))
                db.commit()
                print("Data Saved to Database")
        else:
            GPIO.output(led,GPIO.HIGH)
            print("ALERT!!!INTRUSION DETECTED AT YOUR HOUSE")
            z= datetime.datetime.now().strftime(dateString)#STORING DATE AND TIME IN A VARIABLE
            print("Date and time of action: ")
            print(z)#PRINTING THE DATE AND TIME OF INTRUSION
            cam.start_preview()
            time.sleep(1)
            cam.capture('/home/pi/Desktop/final/Images/%s.jpg'%str(z))
            time.sleep(1)
            cam.stop_preview()
            path='/home/Desktop/final/Images/img.jpg' #DATABASE SECTION
            db=MySQLdb.connect("localhost","root","xaviers123","datalog")
            curs=db.cursor()
            with db:
                curs.execute("""INSERT into intruderlog values (%s,%s)""",(z,path))
                db.commit()
                print("Data Saved to Database")
            fromaddr = "raghvendra7312@gmail.com" #EMAIL SECTION
            toaddr = "raghvendradamle894@gmail.com@.com"
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "INTRUDER ALERT"
            body = "Intruder Has Been Detected in Front of House "+str(z)
            msg.attach(MIMEText(body, 'plain'))
            filename = str(z)+".jpg"
            attachment = open('/home/pi/Desktop/final/Images/%s.jpg'%str(z),"rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "RealAxe#478")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            print("CHECK YOUR MAIL FOR THE ATTACHMENT OF THE INTRUDER")
GPIO.cleanup()
