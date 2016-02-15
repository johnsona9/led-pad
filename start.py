""" Starting file for the led-pad lock. File handles all top level aspects. """
import time
import subprocess
import uuid
import thread
import random

import picamera
import RPi.GPIO as GPIO
from multiprocessing import Process

import colors
import buttonScan

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(5, GPIO.IN)
GPIO.setup(3, GPIO.OUT)


camera = picamera.PiCamera()
randomColors = [[True, False, False], [False, True, False], [False, False, True], [True, True, False], [True, False, True], [False, True, True]]
password = [[True, False, True], [False, True, True], [False, True, True], [False, False, True], [True, False, False], [False, True, False]]
#purple, teal, teal, blue, red, green
yCoords = [7, 11, 13, 15]
xCoords = [40, 38, 36, 32]

def main():
    initialTime = time.time()
    run(initialTime)
    while 1:
        checkMotion()

def run(initialTime):
	print "new run"
	matrix = randomizeMatrix()
	lastScan = 0
	combination = []
	switchTime = 0
	while int(time.time() - initialTime) < 60:
		colors.handleColors(matrix, 0.0005)
		x = buttonScan.scan()
		if (lastScan is None and x is not None):
			lastScan = x
			combination.append(getColorValue(matrix, x))
			if len(combination) is 6:
				switchTime = int(time.time() - initialTime)
				matrix = checkPassword(combination)
				combination = []
		elif (lastScan is not None and x is None):
			lastScan = x
		if int(time.time() - initialTime) % 7 == 0 and switchTime != int(time.time() - initialTime):
			switchTime = int(time.time() - initialTime)
			matrix = randomizeMatrix()
			GPIO.output(3, False)

def randomizeMatrix():
	final = [[], [], [], []]
	for x in range(0, len(final)):
		for y in range(0, 4):
			final[x].append(random.choice(randomColors))
	return final

def getColorValue(matrix, buttonPressed):
	x = xCoords.index(buttonPressed[1])
	y = yCoords.index(buttonPressed[0])
	return matrix[x][y]

def checkPassword(combo):
	print "checking"
	if combo == password:
		matrix = singleColor([False, True, False])
		GPIO.output(3, True)
	else:
		matrix = singleColor([True, False, False])
		thread.start_new_thread(handleNotification, ())
	return matrix

def singleColor(color):
	final = [[], [], [], []]
	for x in range(0, len(final)):
		for y in range(0, 4):
			final[x].append(color)
	return final

def handleNotification():
	name = "image_" + str(uuid.uuid4()) + ".jpg"
	camera.capture(name)
	subprocess.call(["./notify.sh " + name], shell=True)

def checkMotion():
    if not GPIO.input(5):
        initialTime = time.time()
        run(initialTime)

main()
