# Imports
import RPi.GPIO as GPIO
import multiprocessing
import sensorDetector
import random
import time

# Variables
clickRotary = 11
dataRotary = 12
button = 16
buttonLED = 18

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(clickRotary, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dataRotary, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buttonLED, GPIO.OUT)


def speedGame():
    totalPoints = 0
    lastAskedSensor = ''
    timeBegin = time.time()

    GPIO.output(buttonLED, GPIO.HIGH)
    sensorDetector.playSound("Audio/start_of_game.mp3")

    while True:
        # Selects a random command
        sensors = ['cover', 'shake', 'twist', 'smack']
        random.shuffle(sensors)
        askedSensor = sensors[0]

        if totalPoints < 10:
            sleepTime = 2.00
        elif totalPoints < 25:
            sleepTime = 1.75
        elif totalPoints < 50:
            sleepTime = 1.50
        elif totalPoints < 100:
            sleepTime = 1.25
        else:
            sleepTime = 1.00

        # Checks if the last command is the same as the new one
        if askedSensor == lastAskedSensor:
            continue

        # Gives a random command using mp3 files.
        print("Asked: " + askedSensor)
        sensorDetector.playSound("Audio/" + askedSensor + ".mp3")

        usedSensor = sensorDetector.sensorDetector(sleepTime)
        print("Used" + usedSensor)

        # Checks is the used sensor is the same as the asked sensor or if the user is too slow
        if usedSensor == askedSensor:
            totalPoints += 1
            print("Points: " + str(totalPoints))
            sensorDetector.playSound("Audio/succes.mp3")
            lastAskedSensor = askedSensor
            continue
        else:
            sensorDetector.playSound("Audio/fail.mp3")
            sensorDetector.playSound("Audio/end_of_game.mp3")
            GPIO.output(buttonLED, GPIO.LOW)

            timePlayed = time.time() - timeBegin

            data = [totalPoints, int(timePlayed)]
            return data


def testCommand(asked):
    print(asked)
    for sensor in range(0, len(asked)):
        usedSensor = sensorDetector.sensorDetector(5)
        print(usedSensor)

        if usedSensor == asked[sensor]:
            sensorDetector.playSound("Audio/succes.mp3")
            continue
        elif asked[sensor] == 'slow':
            return False
        else:
            return False

    return True


def memoryGame():
    totalPoints = 0
    askedSensors = []
    timeBegin = time.time()

    GPIO.output(buttonLED, GPIO.HIGH)
    sensorDetector.playSound("Audio/start_of_game.mp3")

    while True:
        sensors = ['smack', 'cover', 'shake', 'twist']
        random.shuffle(sensors)
        askedSensors.append(sensors[0])

        for sensor in range(0, len(askedSensors)):
            sensorDetector.playSound("Audio/" + askedSensors[sensor] + ".mp3")

        doneCorrect = testCommand(askedSensors)

        if doneCorrect:
            totalPoints += 1
            continue
        else:
            sensorDetector.playSound("Audio/fail.mp3")
            sensorDetector.playSound("Audio/end_of_game.mp3")
            GPIO.output(buttonLED, GPIO.LOW)

            timePlayed = time.time() - timeBegin
            timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

            data = [totalPoints, int(timePlayed), timeNow]
            return data


def testing():
    testSensors = ['cover', 'shake', 'twist', 'smack']
    testedSensors = [False, False, False, False]

    for commands in range(4):
        while True:
            sensorDetector.playSound("Audio/" + testSensors[commands] + ".mp3")

            usedSensor = sensorDetector.sensorDetector(10)

            if usedSensor == testSensors[commands]:
                sensorDetector.playSound("Audio/succes.mp3")
                testedSensors[commands] = True
                time.sleep(1)
                break
            elif usedSensor == 'slow':
                sensorDetector.playSound("Audio/fail.mp3")
                testedSensors[commands] = False
                break
            else:
                sensorDetector.playSound("Audio/fail.mp3")
                continue

    return testedSensors


if __name__ == "__main__":
    print(testing())
