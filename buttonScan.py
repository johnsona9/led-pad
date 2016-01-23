import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

btnSelect = [7, 11, 13, 15]
btnIn = [40, 38, 36, 32]

for x in btnSelect:
	GPIO.setup(x, GPIO.OUT)
	GPIO.output(x, True)
for x in btnIn:
	GPIO.setup(x, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(40, GPIO.FALLING, bouncetime = 500)
GPIO.add_event_detect(38, GPIO.FALLING, bouncetime = 500)
GPIO.add_event_detect(36, GPIO.FALLING, bouncetime = 500)
GPIO.add_event_detect(32, GPIO.FALLING, bouncetime = 500)
def scan():
	for x in btnSelect:
		GPIO.output(x, False)
		for y in btnIn:
			if not GPIO.input(y):
				return (x, y)
		GPIO.output(x, True)
