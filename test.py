
import RPi.GPIO as GPIO

#Constants
r = 'going: '

#Set up GPIOs
GPIO.setmode(GPIO.BOARD)

# set up GPIO pins
GPIO.setup(7, GPIO.OUT) #Forward
GPIO.setup(11, GPIO.OUT) #Backward
GPIO.setup(12, GPIO.OUT) #Left
GPIO.setup(13, GPIO.OUT) #Right

#Make sure the rest are disabled
GPIO.output(7,GPIO.HIGH)
GPIO.output(11,GPIO.LOW)
GPIO.output(12,GPIO.LOW)
GPIO.output(13,GPIO.LOW)

while True:
	print 'test'