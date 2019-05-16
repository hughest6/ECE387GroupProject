# ECE 387 final group project
# Program to initiate and make use of accelerometer

import time
import board
import busio
import adafruit_mma8451
import statistics


i2c = busio.I2C(board.SCL,board.SDA)


sensor = adafruit_mma8451.MMA8451(i2c)

x=0
y=0
z=0

meanX = 0
meanY = 0
meanZ = 0

def refreshValues():
    global x, y, z

    x, y, z = sensor.acceleration


def getXAcceleration():
    global x
    refreshValues()
    return x


def getYAcceleration():
    global y
    refreshValues()
    return y

def getZAcceleration():
    global z
    refreshValues()
    return z


def calibrate():
    global meanX, meanY, meanZ
    meanX = calX()
    meanY = calY()
    meanZ = calZ()


def calX():

    sample = []
    i = 0
    while i < 100:
        sample.append(getXAcceleration())
        i += 1

    return statistics.mean(sample)


def calY():
    sample = []
    i = 0
    while i < 100:
        sample.append(getXAcceleration())
        i += 1

    return statistics.mean(sample)


def calZ():
    sample = []
    i = 0
    while i < 100:
        sample.append(getXAcceleration())
        i += 1

    return statistics.mean(sample)
