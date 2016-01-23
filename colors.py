import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

red = [37, 35, 33, 31]
green = [26, 24, 22, 18]
blue = [29, 23, 21, 19]
cath = [8, 10, 12, 16]

testMatrix = [[[True, True, True], [True, False, True], [False, False, True], [True, True, False]], [[False, True, False], [False, True, True], [False, False, True], [False, True, False]], [[True, False, False], [False, False, True], [False, False, True], [False, True, True]], [[False, True, False], [True, False, False], [True, False, False], [False, False, True]]]

for x in red:
	GPIO.setup(x, GPIO.OUT)
	GPIO.output(x, False)
for x in green:
	GPIO.setup(x, GPIO.OUT)
	GPIO.output(x, False)
for x in blue:
	GPIO.setup(x, GPIO.OUT)
	GPIO.output(x, False)
for x in cath:
	GPIO.setup(x, GPIO.OUT)
	GPIO.output(x, True)

def off():
	for x in red:
		GPIO.output(x, False)
	for x in green:
		GPIO.output(x, False)
	for x in blue:
		GPIO.output(x, False)
	for x in cath:
		GPIO.output(x, True)
			
def cathodesUp():
	for x in cath:
		GPIO.output(x, True)

# This function takes in a 3-dimensional array
# rows, columns, and colors are the dimensions
def handleColors(colorMatrix, sleep):
	for row in range(0, len(colorMatrix)):
		for column in range(0, len(colorMatrix[row])):
			GPIO.output(cath[column], False)
			GPIO.output(red[row], colorMatrix[row][column][0])
			GPIO.output(green[row], colorMatrix[row][column][1])
			GPIO.output(blue[row], colorMatrix[row][column][2])
			time.sleep(sleep)
			GPIO.output(cath[column], True)
			GPIO.output(red[row], False)
			GPIO.output(green[row], False)
			GPIO.output(blue[row], False)

