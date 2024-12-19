# Imports
import RPi.GPIO as GPIO
import FaBo9Axis_MPU9250
import time
import multiprocessing
import pygame

# Variables
mpu9250 = FaBo9Axis_MPU9250.MPU9250()  # this variables is the GPIO setup for the accelerometer

ldr = 7
clickRotary = 11
dataRotary = 12
button = 16

accelCap = 1.5
diffCap = 80


def playSound(audioFile):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audioFile)
    pygame.mixer.music.play(0)

    while pygame.mixer.music.get_busy():
        continue


# Counts if the user is too slow
def SLOW(sleepTime):
    time.sleep(sleepTime)
    return


# Checks if the button is pressed
def BUT():
    while True:
        if GPIO.input(button):
            return


# Checks if the rotary encoder is twisted
def ENC():
    clickLastState = GPIO.input(clickRotary)

    while True:
        clickState = GPIO.input(clickRotary)
        dataState = GPIO.input(dataRotary)

        if clickState != clickLastState or dataState != clickState:
            return
        clickLastState = clickState
        time.sleep(0.01)


# Checks is the accelerometer is moving in every axel
def ACC():
    while True:
        accel = mpu9250.readAccel()
        for i in accel:
            if accel[i] >= accelCap or accel[i] <= -accelCap:
                return


# checks if the charge time is higher than the differential cap
def LDR():
    while True:
        GPIO.setup(ldr, GPIO.OUT)
        GPIO.output(ldr, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(ldr, GPIO.IN)
        currentTime = time.time()
        diff = 0

        while GPIO.input(ldr) == GPIO.LOW:
            diff = (time.time() - currentTime) * 1000

            if diff > diffCap:
                return


# Main function for the sensor detector
def sensorDetector(sleepTime):
    # puts all the functions above in a array
    processes = [multiprocessing.Process(name='cover', target=LDR),
                 multiprocessing.Process(name='shake', target=ACC),
                 multiprocessing.Process(name='twist', target=ENC),
                 multiprocessing.Process(name='smack', target=BUT),
                 multiprocessing.Process(name='slow', target=SLOW, args=(sleepTime,))]

    # starts all the process
    for process in processes:
        process.start()

    # Loop to check if one of the process is still processing
    loopDone = False
    while not loopDone:
        for process in processes:
            if not process.is_alive():
                usedSensor = process.name
                loopDone = True

    # Kills all the process
    for process in processes:
        process.terminate()

    return usedSensor
