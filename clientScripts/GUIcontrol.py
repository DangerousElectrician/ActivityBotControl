import sys
import tkinter
import robotControl
import math
import numpy as np
from pylab import *

top = tkinter.Tk()
rob = robotControl.robotControl(sys.argv[1], 9600, timeout=4)

ticks = [0,0]
whisker = [0,0]
ping = 0

def readSensors():
	rob.updateSensors()
	ticks = rob.getTicks()
	ping = rob.getPing()
	whisker = rob.getWhisker()
	#print("p "+str(ping)+"\ttl "+str(ticks[0])+"\ttr "+str(ticks[1])+"\twl "+str(whisker[0])+"\twr "+str(whisker[1]))
	#print(str(math.degrees(rob.getTheta())))
	top.after(1,readSensors)

def startMotor():
	rob.driveSpeed(-5,5)

def stopMotor():
	rob.driveSpeed(0,0)
	
ra= []
th = []
def printData():
	startMotor()
	print(str(math.degrees(rob.getTheta()))+"\t"+str(rob.getPing()))
	ra.append(rob.getPing())
	th.append(rob.getTheta())
	if(rob.getTheta()>2*math.pi):
		stopMotor()
		print(ra,th)
		
		r= np.array(ra)
		theta = np.array(th)

		ax = subplot(111, polar=True)
		c = scatter(theta, r)
		plt.show()
	else:
		top.after(1,printData)
	
	
B = tkinter.Button(top, text ="spin", command = startMotor)
B2 = tkinter.Button(top, text ="stop", command = stopMotor)
B3 = tkinter.Button(top, text ="scan", command = printData)


B.pack()
B2.pack()
B3.pack()
top.after(1,readSensors)
top.mainloop()
