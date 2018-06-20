
import RPi.GPIO as GPIO
import time
import urllib2

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
GPIO.output(11,GPIO.HIGH)
GPIO.output(12,GPIO.HIGH)
GPIO.output(13,GPIO.HIGH)



#GPIO directions
def forward():
    #Set the direction of Motor A
    GPIO.output(11,GPIO.HIGH) # Stop backward
    GPIO.output(7, GPIO.LOW) # Go forward
    
def backward():
    #Set the direction of Motor A
    GPIO.output(7, GPIO.HIGH) #Stop forward
    GPIO.output(11, GPIO.LOW) #Go backward
 
def right():
    #Set the direction of Motor B
    GPIO.output(12,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)

def left():
    #Set the direction of Motor B
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(12,GPIO.LOW)
    
def still_f_b():
    GPIO.output(11,GPIO.HIGH) # Stop backward
    GPIO.output(7, GPIO.HIGH) # Stop forward
    
def still_l_r():
    GPIO.output(12,GPIO.HIGH)
    GPIO.output(13,GPIO.HIGH)
#end of direction functions



try:
	while True:
	    data = urllib2.urlopen("http://165.227.144.106:8080/getDirection").read()
	    if data == 'S':
	        print('%s [Still]' % r)
	        still_f_b()
	        still_l_r()
	    elif data == 'F':
	        print('%s [Forward]' % r)
	        forward()
	        still_l_r()
	    elif data == 'B':
	        print('%s [Backward]' % r)
	        backward()
	        still_l_r()
	    elif data == 'L':
	        print('%s [Left]' % r)
	        still_f_b()
	        left()
	    elif data == 'R':
	        print('%s [Right]' % r)
	        still_f_b()
	        right()
	    elif data == 'FL':
	        print('%s [Forward Left]' % r)
	        forward()
	        left()
	    elif data == 'FR':
	        print('%s [Forward Right]' % r)
	        forward()
	        right()
	    elif data == 'BL':
	        print('%s [Backward Left]' % r)
	        backward()
	        left()
	    elif data == 'BR':
	        print('%s [Backward Right]' % r)
	        backward()
	        right()
	    elif data == 'SD':
	        print('Setting GPIOs to LOW')
	        still_f_b()
	        still_l_r()
	        print('Disconnecting')
	        client_sock.close()
	        server_sock.close()
	        print('Shutting down')
	        os.system('halt')
	    
except IOError:
print('Disconnecting')
client_sock.close()
server_sock.close()
pass
    

