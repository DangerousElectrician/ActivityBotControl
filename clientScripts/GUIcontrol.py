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

global updateSensors
updateSensors = False
def readSensors():
	rob.updateSensors()
	if(updateSensors):
		top.after(50,readSensors)
		
def stopReadSensors():
	global updateSensors
	updateSensors = False
	
def startReadSensors():
	global updateSensors
	updateSensors = True
	top.after(1, readSensors)
	
h, = plot([], [], 'bo')
def update_line(hl, new_datax, new_datay):
	hl.set_xdata(np.append(hl.get_xdata(), new_datax))
	hl.set_ydata(np.append(hl.get_ydata(), new_datay))
	gca().relim()
	gca().autoscale_view()
	axis('equal')
	draw()

	
global stopScan
stopscan = False
def startPlot():
	ion()
	show()
	#rob.driveSpeed(-5,5)
	global stopScan
	stopScan = False
	plotData(rob.getTheta())

	
#ra= []
#th = []
def plotData(initth):
	#print(str(math.degrees(rob.getTheta()))+"\t"+str(rob.getPing()))
	#ra.append(rob.getPingcm())
	#th.append(rob.getTheta())
	print(rob.getPingcm())
	update_line(h, rob.getPingcm()*cos(rob.getTheta())+(rob.getPos()[0])/3.25, rob.getPingcm()*sin(rob.getTheta())+(rob.getPos()[1])/3.25)
	if(not stopScan):#(rob.getTheta()-initth)>2*math.pi):
		#rob.driveSpeed(0,0)
		#print(ra,th)
		
		#r= np.array(ra)
		#theta = np.array(th)

		#ax = subplot(111, polar=True)
		#c = scatter(theta, r)
		#plt.show()
	#else:
		top.after(50,lambda:plotData(initth))
	
def stopScn():
	global stopScan
	stopScan= True
	
def main():
	frame = tkinter.Frame(top)#, width=200, height=100)
	Binit = tkinter.Button(frame, text ="init", command = init, height = 5, width = 10)
	Bscan = tkinter.Button(frame, text ="scan", command = startPlot, height = 5, width = 10)
	Bsscan = tkinter.Button(frame, text ="stop scan", command = stopScn, height = 5, width = 10)
	Boff = tkinter.Button(frame, text ="off", command = off, height = 5, width = 10)
	Breset = tkinter.Button(frame, text ="reset", command = rob.reset, height = 5, width = 10)
	BstartWander = tkinter.Button(frame, text ="wander", command = rob.startWander, height = 5, width = 10)
	BstopWander = tkinter.Button(frame, text ="stop wander", command = rob.stopWander, height = 5, width = 10)
	BstartReadSensors = tkinter.Button(frame, text ="update\nsensors", command = startReadSensors, height = 5, width = 10)
	BstopReadSensors = tkinter.Button(frame, text ="stop update\nsensors", command = stopReadSensors, height = 5, width = 10)
		
	speed = 15
	direcOn = [False,False,False,False]
	def goforward(e):
		if(not direcOn[0]):
			rob.driveSpeed(speed,speed)
			direcOn[0]=True
	def stopforward(e):
		if(not (direcOn[1] or direcOn[2] or direcOn[3])):
			rob.driveSpeed(0,0)
		direcOn[0]=False
		
	def gobackward(e):
		if(not direcOn[1]):
			rob.driveSpeed(-speed,-speed)	
			direcOn[1]=True
	def stopbackward(e):
		if(not (direcOn[0] or direcOn[2] or direcOn[3])):
			rob.driveSpeed(0,0)
		direcOn[1]=False
		
	def goleft(e):
		if(not direcOn[2]):
			rob.driveSpeed(-speed,speed)	
			direcOn[2]=True
	def stopleft(e):
		if(not (direcOn[1] or direcOn[0] or direcOn[3])):
			rob.driveSpeed(0,0)
		direcOn[2]=False
		
	def goright(e):
		if(not direcOn[3]):
			rob.driveSpeed(speed,-speed)	
			direcOn[3]=True
	def stopright(e):
		if(not (direcOn[1] or direcOn[2] or direcOn[0])):
			rob.driveSpeed(0,0)
		direcOn[3]=False
	
	frame.bind("<KeyRelease-w>", stopforward)
	frame.bind("<KeyPress-w>", goforward)
	frame.bind("<KeyRelease-a>", stopleft)
	frame.bind("<KeyPress-a>", goleft)
	frame.bind("<KeyRelease-s>", stopbackward)
	frame.bind("<KeyPress-s>", gobackward)
	frame.bind("<KeyRelease-d>", stopright)
	frame.bind("<KeyPress-d>", goright)
	frame.focus_set()
	
	Binit.grid(row=0, column=0)
	Boff.grid(row=0, column=1)
	BstartReadSensors.grid(row=1, column=0)
	BstopReadSensors.grid(row=1, column=1)
	Bscan.grid(row=2, column=0)
	Bsscan.grid(row=2, column=1)
	BstartWander.grid(row=3, column=0)
	BstopWander.grid(row=3, column=1)
	Breset.grid(row=4, column=0)

	frame.pack()
	top.mainloop()
	
main()
