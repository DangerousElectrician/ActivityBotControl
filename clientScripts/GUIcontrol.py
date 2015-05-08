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

def readSensors():
	rob.updateSensors()
	top.after(1,readSensors)
	
ion()
h, = plot([], [], 'bo')
def update_line(hl, new_datax, new_datay):
	hl.set_xdata(np.append(hl.get_xdata(), new_datax))
	hl.set_ydata(np.append(hl.get_ydata(), new_datay))
	gca().relim()
	gca().autoscale_view()
	draw()

	
def startPlot():
	rob.driveSpeed(-5,5)
	plotData(rob.getTheta())

	
ra= []
th = []
def plotData(initth):
	#print(str(math.degrees(rob.getTheta()))+"\t"+str(rob.getPing()))
	ra.append(rob.getPingcm())
	th.append(rob.getTheta())
	update_line(h, rob.getPingcm()*cos(rob.getTheta()), rob.getPingcm()*sin(rob.getTheta()))
	if((rob.getTheta()-initth)>2*math.pi):
		rob.driveSpeed(0,0)
		#print(ra,th)
		
		r= np.array(ra)
		theta = np.array(th)

		ax = subplot(111, polar=True)
		c = scatter(theta, r)
		plt.show()
	else:
		top.after(1,lambda:plotData(initth))
	

	
def main():
	Binit = tkinter.Button(top, text ="init", command = init)
	B3 = tkinter.Button(top, text ="scan", command = startPlot)
	Boff = tkinter.Button(top, text ="off", command = off)
	Breset = tkinter.Button(top, text ="reset", command = rob.reset)

		
	speed = 15
	def goforward(e):
		rob.driveSpeed(speed,speed)	
	def stopforward(e):
		rob.driveSpeed(0,0)
		
	def gobackward(e):
		rob.driveSpeed(-speed,-speed)	
	def stopbackward(e):
		rob.driveSpeed(0,0)
		
	def goleft(e):
		rob.driveSpeed(-speed,speed)	
	def stopleft(e):
		rob.driveSpeed(0,0)
		
	def goright(e):
		rob.driveSpeed(speed,-speed)	
	def stopright(e):
		rob.driveSpeed(0,0)
	
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
	B3.pack()
	Breset.pack()
	top.after(1,readSensors)
	top.mainloop()
	
main()
