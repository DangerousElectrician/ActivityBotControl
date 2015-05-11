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
xbuf=[]
ybuf=[]
xposbuf=[]
yposbuf=[]
def readSensors():	#retrieves sensor data from robot
	rob.updateSensors()
	xbuf.append(rob.getPingcm()*cos(rob.getTheta())+(rob.getPos()[0])/3.25)
	ybuf.append(rob.getPingcm()*sin(rob.getTheta())+(rob.getPos()[1])/3.25)
	xposbuf.append(rob.getPos()[0]/3.25)
	yposbuf.append(rob.getPos()[1]/3.25)
	print(rob.getPingcm())
	if(updateSensors):
		top.after(1,readSensors)
		
def stopReadSensors():
	global updateSensors
	updateSensors = False
	
def startReadSensors():
	global updateSensors
	updateSensors = True
	top.after(1, readSensors)
	
h,g = plot([], [], 'ro',[],[],'bs') #THIS LINE IS CAUSING PROBLEMS WITH CLOSING THE PROGRAM
def update_line(hl, new_datax, new_datay):	#draws more points on graph
	hl.set_xdata(np.append(hl.get_xdata(), new_datax))
	hl.set_ydata(np.append(hl.get_ydata(), new_datay))
	gca().relim()
	gca().autoscale_view()
	gca().set_aspect('equal', 'datalim', 'C')
	gca().apply_aspect()
	draw()
	

	
global stopScan
stopscan = False
def startPlot():
	ion()
	show()
	global stopScan
	stopScan = False
	plotData(rob.getTheta())

	
def plotData(initth):	#does some of the data handling for graphing
	update_line(h, xbuf, ybuf)
	xbuf.clear()
	ybuf.clear()
	update_line(g,xposbuf,yposbuf)
	yposbuf.clear()
	xposbuf.clear()
	if(not stopScan):
		top.after(200,lambda:plotData(initth))
	
def stopScn():
	global stopScan
	stopScan= True
	ioff()
	
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
	def quit():
		close()
		#top.destroy()
	top.protocol("WM_DELETE_WINDOW", quit)
	top.mainloop()
	
main()
