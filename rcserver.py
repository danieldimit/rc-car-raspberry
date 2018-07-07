# file: rcserver.py
# auth: Daniel Dimitrov <daniel.dimitrov@campus.tu-berlin.de>, Radoslav Vlaskovski
# desc: Program that can connect to a customly build android app via Bluetooth and to a custom controlling server via Internet

import RPi.GPIO as GPIO
import time
import threading
from bluetooth import *
import urllib2

#Constants
r = 'going: '

#Set up GPIOs
GPIO.setmode(GPIO.BOARD)

# set up GPIO motor controlling pins
GPIO.setup(7, GPIO.OUT) #Forward
GPIO.setup(11, GPIO.OUT) #Backward
GPIO.setup(12, GPIO.OUT) #Left
GPIO.setup(13, GPIO.OUT) #Right

#Set up GPIO bluetooth-WiFi toggling
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

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

def decide_direction(data):
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

#Bluetooth control thread
def bluetooth_worker():
    toggle = 0;

    # Listener for the button changed event
    try:
        while True:

            print("loop bluetooth")
            #Try to connect via Bluetooth
            server_sock=BluetoothSocket( RFCOMM )
            server_sock.bind(("",PORT_ANY))
            server_sock.listen(1)

            port = server_sock.getsockname()[1]

            uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

            advertise_service(server_sock, "SampleServer", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ])       
            print("Waiting for phone to engage connection %d" % port)

            #BluetoothSocket.accept() is a blocking call
            client_sock, client_info = server_sock.accept()
            print("Accepted connection from ", client_info)
            # Everything is setup so just get the command and drive the car
            try:
                while True:
                    if (toggle == 0):
                        data = client_sock.recv(1024)
                        decide_direction(data)
                    else:
                        time.sleep(0.01)
                        GPIO.wait_for_edge(15, GPIO.FALLING)
                        time.sleep(0.01)
                        GPIO.wait_for_edge(15, GPIO.RISING)
                        toggle = 0 if toggle == 1 else 1
            except IOError:
                print('Disconnecting')
                client_sock.close()
                server_sock.close()
                pass
    except KeyboardInterrupt:  
        GPIO.cleanup()
    return

def wifi_worker():
    toggle = 0;

    # Listener for the button changed event
    try:
        while True:

            print("loop wifi")

            if (toggle == 1):
                data = urllib2.urlopen("http://165.227.144.106:8080/getDirection").read()
                decide_direction(data)
            else:
                time.sleep(0.01)
                GPIO.wait_for_edge(15, GPIO.FALLING)
                print("PAST THIS")
                time.sleep(0.01)
                GPIO.wait_for_edge(15, GPIO.RISING)
                print("PAST RISING")
                toggle = 0 if toggle == 1 else 1
            
    except KeyboardInterrupt:  
        GPIO.cleanup()
    return

#Start the bluetooth thread
t_bt = threading.Thread(target=bluetooth_worker)
t_bt.start()

#Start the wifi service in this thread
wifi_worker()