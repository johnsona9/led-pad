""" Starting file for the led-pad lock. File handles all top level aspects. """
import time
<<<<<<< HEAD
import random
import thread
import subprocess
import uuid

import picamera
import RPi.GPIO as GPIO

import colors
import buttonScan

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(5, GPIO.IN)
GPIO.setup(3, GPIO.OUT)
CAMERA = picamera.PiCamera()
RANDOM_COLORS = [[True, False, False], [False, True, False], [False, False, True], [True, True, False], [True, False, True], [False, True, True]]
PASSWORD = [[True, False, True], [False, True, True], [False, True, True], [False, False, True], [True, False, False], [False, True, False]]
# purple, teal, teal, blue, red, green
Y_COORDS = [7, 11, 13, 15]
X_COORDS = [40, 38, 36, 32]

def main():
    initialTime = time.time()
    run(initialTime)
    while 1:
        check_motion()

def run(initialTime):
    matrix = randomize_matrix()
    lastScan = (0, 0)
    combination = []
    switchTime = 0
    while int(time.time() - initialTime) < 60:
        colors.handleColors(matrix, 0.0005)
        x = buttonScan.scan()
        if lastScan is None and x is not None:
            lastScan = x
            combination.append(get_color_value(matrix, x))
            if len(combination) is 6:
                matrix = check_password(combination)
                combination = []
                initialTime = time.time()
        elif lastScan is not None and x is None:
            lastScan = x
        if int(time.time() - initialTime) % 7 == 0 and switchTime != int(time.time() - initialTime):
            switchTime = int(time.time() - initialTime)
            matrix = randomize_matrix()
            GPIO.output(3, False)

def randomize_matrix():
    final = [[], [], [], []]
    for x in range(0, len(final)):
        for y in range(0, 4):
            final[x].append(random.choice(RANDOM_COLORS))
    return final

def get_color_value(matrix, buttonPressed):
    x = X_COORDS.index(buttonPressed[1])
    y = Y_COORDS.index(buttonPressed[0])
    return matrix[x][y]

def check_password(combo):
    if combo == PASSWORD:
        matrix = single_color([False, True, False])
        GPIO.output(3, True)
    else:
        matrix = single_color([True, False, False])
        thread.start_new_thread(handle_notification, ())
    return matrix

def single_color(color):
    final = [[], [], [], []]
    for x in range(0, len(final)):
        for y in range(0, 4):
            final[x].append(color)
    return final

def handle_notification():
    name = "image_" + str(uuid.uuid4()) + ".jpg"
    CAMERA.capture(name)
    subprocess.call(["./notify.sh " + name], shell=True)

def check_motion():
    if not GPIO.input(5):
        initialTime = time.time()
        run(initialTime)

main()
