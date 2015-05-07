import sys
import tkinter
import robotControl
import math
import numpy as np
from pylab import *

top = tkinter.Tk()
rob = robotControl.robotControl(sys.argv[1], 9600, timeout=4)

def init():
	rob.startSensors()
	rob.startDrive()
	
def off():
	rob.stopSensors()
	rob.stopDrive()

	
def startPlot():
	plotData(rob.getTheta())

def readSensors():
	rob.updateSensors()
	top.after(1,readSensors)
	
ra= []
th = []
def plotData(initth):
	rob.driveSpeed(-5,5)
	print(str(math.degrees(rob.getTheta()))+"\t"+str(rob.getPing()))
	ra.append(rob.getPing())
	th.append(rob.getTheta())
	if((rob.getTheta()-initth)>2*math.pi):
		rob.driveSpeed(0,0)
		print(ra,th)
		
		r= np.array(ra)
		theta = np.array(th)

		ax = subplot(111, polar=True)
		c = scatter(theta, r)
		plt.show()
	else:
		top.after(1,lambda:plotData(initth))
	
def main():
	B = tkinter.Button(top, text ="init", command = init)
	B3 = tkinter.Button(top, text ="scan", command = startPlot)
	B2 = tkinter.Button(top, text ="off", command = off)
	Breset = tkinter.Button(top, text ="reset", command = rob.reset)

	B.pack()
	B2.pack()
	B3.pack()
	Breset.pack()
	top.after(1,readSensors)
	top.mainloop()
	
main()
