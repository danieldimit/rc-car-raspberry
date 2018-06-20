# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

import RPi.GPIO as GPIO
import time
import urllib2
contents = urllib2.urlopen("https://jsonplaceholder.typicode.com/posts/1").read()

print contents

