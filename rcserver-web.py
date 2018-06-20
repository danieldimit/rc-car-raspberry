
import RPi.GPIO as GPIO
import time
import urllib2


while true:
    contents = urllib2.urlopen("http://165.227.144.106:8080/getDirection").read()
    print contents

