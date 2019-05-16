# ECE 387 final group project
# Program to initate and make use of neural network
# Copyright: Tyler Hughes

import numpy as np
import neuralNetwork
import time
import keyboard
import Calculations
import serial
import re

ser=serial.Serial("/dev/ttyACM0",9600)
ser.baudrate=9600

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()




if __name__ == "__main__":
    
	epochs = 150		# network iterations
	
	# Load swing data
	swing_data = open("swingdataupdated.txt", "r")
	input_array = np.loadtxt(swing_data, delimiter=';')
	print("NN training data successfully opened")
	# Load corrisponding swing type
	swing_type = open("punchtype.txt", "r")
	y_array = np.loadtxt(swing_type, delimiter=';')
	print("Swingtype expected outputs succesfully opened")

	# load data into three separate arrays to make use of network
	xarr = np.array(input_array[0:49])
	yarr = np.array(input_array[50:99])
	zarr = np.array(input_array[100:149])
	x = np.array([xarr,yarr,zarr])
	y = np.zeros((3,1))
	nn = neuralNetwork.NeuralNetwork(x,y)
	
	# iterate through epochs
	print("Initializing Neural Network")
	printProgressBar(0, epochs, prefix = 'NN Training Progress:', suffix = 'Complete', length = 50)
	for i in range(epochs):
		# during each epoch, train net with entire data set
		for j in range(1,59):
			# Calculate relative 0 of x array
			b_index = j * 150
			yval = y_array[j]
			# Generate x and y arrays from dat files
			xarr = np.array(input_array[b_index:b_index+49])
			yarr = np.array(input_array[b_index+50:b_index+99])
			zarr = np.array(input_array[b_index+100:b_index+149])
			xload = np.array([xarr,yarr,zarr])
			yload = np.array([[yval],[yval],[yval]])
			# Load values into network
			nn.loadxy(xload,yload)
			# Network Traversal
			nn.feedforward()
			nn.backprop()
		printProgressBar(i+1, epochs, prefix = 'NN Training Progress:', suffix = 'Complete', length = 50)
	print("Network Initialization Complete!")
	print("Calabrating acceloremeter")
	# Calibrate acceloremeter to relative 0
	Calculations.calibrate()
	print("Calibration complete")
	print("Get ready to swing!")
	time.sleep(1)
	print("3!")
	time.sleep(1)
	print("2!")
	time.sleep(1)
	print("1!")
	time.sleep(1)
	print("Swing!")
	
	# Read in new swing data for use in neural network
	loopcount = 0
	sampnum = 50
	arrx = []
	arry = []
	arrz = []
	force_min = 1024
	for k in range(1,100):
		ser.readline()
	for i in range(sampnum):
		arrx.append(Calculations.getXAcceleration())
		arry.append(Calculations.getYAcceleration())
		arrz.append(Calculations.getZAcceleration())
		force_data = ser.readline().decode()
		force_array = [int(s) for s in re.findall(r'\d+', force_data)]
		if np.amin(force_array) < force_min:
			force_min = np.amin(force_array)
		time.sleep(0.01)
	swingx = [[arrx],[arry],[arrz]]
	# Propagate new swing data through network
	nn.loadx(swingx)
	nn.feedforward
	print(nn.output)
	# now determine swing type 
	# method below is not perfect, was determined by examining the network
	# output over the entirety of the training data
	min = 3
	type = 3
	outputsum = np.sum(nn.output)
	if abs(outputsum - 3) < min:
		min = abs(outputsum - 3)
		type = 2
	if abs(outputsum - 2.6) < min:
		min = abs(outputsum - 2.6)
		type = 1
	if abs(outputsum - 2.2) < min:
		min = abs(outputsum - 2.2)
		type = 0
	if type == 0:
		print("You threw a jab!")
	elif type == 1:
		print("You threw a hook!")
	else:
		print("You threw an uppercut!")
	
	# Print punch force relative to sensor ratings
	punchstrength = (1024 - force_min) / 10
	print("Force exerted ", punchstrength, " pounds!")
