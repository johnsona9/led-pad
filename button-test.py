import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

btnSelect = [15, 13, 11, 7]
btnIn = [40, 38, 36, 32]

for x in btnSelect:
	GPIO.setup(x, GPIO.OUT)
	GPIO.output(x, True)
for x in btnIn:
	GPIO.setup(x, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def scan():
	while 1:
		for x in btnSelect:
			GPIO.output(x, False)
			for y in btnIn:
				if not GPIO.input(y):
					print "(" + str(x) + ", " + str(y) + ")"
					return (x, y)
			GPIO.output(x, True)
