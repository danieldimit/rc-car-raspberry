import RPi.GPIO as GPIO
import time
from bluetooth import *
import os

class BluetoothRCServer:

    # Constants
    r = 'going: '

    def __init__(self):
        self.gpio_init()

        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        # Bluetooth
        server_sock = BluetoothSocket(RFCOMM)
        server_sock.bind(("", PORT_ANY))
        server_sock.listen(1)
        port = server_sock.getsockname()[1]

        advertise_service(server_sock, "SampleServer",
                          service_id=uuid,
                          service_classes=[uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE],
                          #                   protocols = [ OBEX_UUID ]
                          )
        print("Waiting for phone to engage connection %d" % port)
        self.client_sock, self.client_info = server_sock.accept()
        print("Accepted connection from ", self.client_info)
        self.listen()


    def listen(self):
        try:
            while True:
                data = self.client_sock.recv(1024)
                if data == 'S':
                    print('%s [Still]' % r)
                    self.still_f_b()
                    self.still_l_r()
                elif data == 'F':
                    print('%s [Forward]' % r)
                    self.forward()
                    self.still_l_r()
                elif data == 'B':
                    print('%s [Backward]' % r)
                    self.backward()
                    self.still_l_r()
                elif data == 'L':
                    print('%s [Left]' % r)
                    self.still_f_b()
                    self.left()
                elif data == 'R':
                    print('%s [Right]' % r)
                    self.still_f_b()
                    self.right()
                elif data == 'FL':
                    print('%s [Forward Left]' % r)
                    self.forward()
                    self.left()
                elif data == 'FR':
                    print('%s [Forward Right]' % r)
                    self.forward()
                    self.right()
                elif data == 'BL':
                    print('%s [Backward Left]' % r)
                    self.backward()
                    self.left()
                elif data == 'BR':
                    print('%s [Backward Right]' % r)
                    self.backward()
                    self.right()
                elif data == 'SD':
                    print('Setting GPIOs to LOW')
                    self.still_f_b()
                    self.still_l_r()
                    print('Disconnecting')
                    self.client_sock.close()
                    self.server_sock.close()
                    print('Shutting down')
                    os.system('halt')

        except IOError:
            pass

    def gpio_init(self):
        # Set up GPIOs
        GPIO.setmode(GPIO.BOARD)

        # set up GPIO pins
        GPIO.setup(7, GPIO.OUT)  # Forward
        GPIO.setup(11, GPIO.OUT)  # Backward
        GPIO.setup(12, GPIO.OUT)  # Left
        GPIO.setup(13, GPIO.OUT)  # Right

        # Make sure the rest are disabled
        GPIO.output(7, GPIO.HIGH)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)

    #GPIO directions
    def forward(self):
        #Set the direction of Motor A
        GPIO.output(11,GPIO.HIGH) # Stop backward
        GPIO.output(7, GPIO.LOW) # Go forward

    def backward(self):
        #Set the direction of Motor A
        GPIO.output(7, GPIO.HIGH) #Stop forward
        GPIO.output(11, GPIO.LOW) #Go backward

    def right(self):
        #Set the direction of Motor B
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(13,GPIO.LOW)

    def left(self):
        #Set the direction of Motor B
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(12,GPIO.LOW)

    def still_f_b(self):
        GPIO.output(11,GPIO.HIGH) # Stop backward
        GPIO.output(7, GPIO.HIGH) # Stop forward

    def still_l_r(self):
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(13,GPIO.HIGH)
    #end of direction functions