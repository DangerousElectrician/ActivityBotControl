import sys
import tkinter
import robotControl
import math
import numpy as np
from pylab import *

top = tkinter.Tk()
rob = robotControl.robotControl(sys.argv[1], 9600, timeout=1)

def init():
	rob.startSensors()
	rob.startDrive()
	
def off():
	rob.stopSensors()
	rob.stopDrive()

def readSensors():
	rob.updateSensors()
	top.after(1,readSensors)
	
h, = plot([], [], 'bo')
def update_line(hl, new_datax, new_datay):
	hl.set_xdata(np.append(hl.get_xdata(), new_datax))
	hl.set_ydata(np.append(hl.get_ydata(), new_datay))
	gca().relim()
	gca().autoscale_view()
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
	print(rob.getPos()[0])
	update_line(h, rob.getPingcm()*cos(rob.getTheta())+(rob.getPos()[0])/3.25, rob.getPingcm()*sin(rob.getTheta())+(rob.getPos()[1])/3.25)
	if(stopScan):#(rob.getTheta()-initth)>2*math.pi):
		rob.driveSpeed(0,0)
		#print(ra,th)
		
		#r= np.array(ra)
		#theta = np.array(th)

		#ax = subplot(111, polar=True)
		#c = scatter(theta, r)
		#plt.show()
	else:
		top.after(1,lambda:plotData(initth))
	
def stopScn():
	global stopScan
	stopScan= True
	
def main():
	Binit = tkinter.Button(top, text ="init", command = init)
	Bscan = tkinter.Button(top, text ="scan", command = startPlot)
	Bsscan = tkinter.Button(top, text ="stop scan", command = stopScn)
	Boff = tkinter.Button(top, text ="off", command = off)
	Breset = tkinter.Button(top, text ="reset", command = rob.reset)

		
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
	
	frame = tkinter.Frame(top, width=100, height=100)
	frame.bind("<KeyRelease-w>", stopforward)
	frame.bind("<KeyPress-w>", goforward)
	frame.bind("<KeyRelease-a>", stopleft)
	frame.bind("<KeyPress-a>", goleft)
	frame.bind("<KeyRelease-s>", stopbackward)
	frame.bind("<KeyPress-s>", gobackward)
	frame.bind("<KeyRelease-d>", stopright)
	frame.bind("<KeyPress-d>", goright)
	frame.focus_set()

	frame.pack()
	
	Binit.pack()
	Boff.pack()
	Bscan.pack()
	Bsscan.pack()
	Breset.pack()
	top.after(1,readSensors)
	top.mainloop()
	
main()
