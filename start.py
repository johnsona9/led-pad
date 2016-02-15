""" Starting file for the led-pad lock. File handles all top level aspects. """
import time
import subprocess
import uuid
import thread
import random

import picamera
import RPi.GPIO as GPIO

import colors
import buttonScan


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(4, GPIO.IN)

CAMERA = picamera.PiCamera()
RANDOM_COLORS = [[True, False, False], [False, True, False], [False, False, True], [True, True, False], [True, False, True], [False, True, True]]
PASSWORD = [[True, False, True], [False, True, True], [False, True, True], [False, False, True], [True, False, False], [False, True, False]]
# purple, teal, teal, blue, red, green
Y_COORDS = [7, 11, 13, 15]
X_COORDS = [40, 38, 36, 32]
INITIAL_TIME = time.time() / 60


def main():
    """ Main function. """
    run()
    while 1:
        checkMotion()


def run():
    """ Function that actually handles work. Runs for 60 seconds before exiting. Gets LED color from button pressed. When 6 buttons are pressed, checks combination. """
    matrix = randomize_matrix()
    last_scan = 0
    combination = []
    while int(time.time() - INITIAL_TIME) < 60:
        colors.handleColors(matrix, 0.0005)
        x = buttonScan.scan()
        if last_scan is None and x is not None:
            last_scan = x
            combination.append(get_color_value(matrix, x))
            if len(combination) is 6:
                matrix = check_password(combination)
                combination = []
                global INITIAL_TIME
                INITIAL_TIME = time.time() / 60
        elif last_scan is not None and x is None:
            last_scan = x
        if int(time.time() - INITIAL_TIME) % 5 == 0:
            matrix = randomize_matrix()

def randomize_matrix():
    """ Function that randomizes the matrix colors. Returns array of arrays of booleans. """
    final = [[], [], [], []]
    for x in range(0, len(final)):
        for y in range(0, 4):
            final[x].append(random.choice(RANDOM_COLORS))
    return final

def get_color_value(matrix, buttonPressed):
    """ Gets the color value of the button that was pressed by the user. """
    x = X_COORDS.index(buttonPressed[1])
    y = Y_COORDS.index(buttonPressed[0])
    return matrix[x][y]

def check_password(combo):
    """ Checks to see if the password entered by the user was correct or incorrect. """
    if combo == PASSWORD:
        matrix = single_color([False, True, False])
    else:
        matrix = single_color([True, False, False])
        thread.start_new_thread(handle_notification, ())
    return matrix

def single_color(color):
    """ Lights the led-pad a single color. """
    final = [[], [], [], []]
    for x in range(0, len(final)):
        for y in range(0, 4):
            final[x].append(color)
    return final

def handle_notification():
    """ Takes picture and runs notification scripts. Uploads to dropbox and sends text. """
    name = "image" + str(uuid.uuid4()) + ".jpg"
    CAMERA.capture(name)
    subprocess.call(["./notify.sh " + name], shell=True)

def check_motion():
    """ Checks to see if there has been motion. If there is then activates the led-pad. """
    if GPIO.input(4):
        global INITIAL_TIME
        INITIAL_TIME = time.time() / 60
        run()


main()
