import tkinter
import serialComs

top = tkinter.Tk()
com = serialComs.serialComs('COM6', 9600, timeout=4)

ticks = []
whisker = []
ping = 0
def helloCallBack():
	com.write(b'v')
	ticks[0] = com.readInt32()
	ticks[1] = com.readInt32()
	ping = com.readInt32()
	whisker[0] = com.readInt32()
	whisker[1] = com.readInt32()
	print("p "+ping+"\twl "+ticks[0]+"\twr "+ticks[1]+"\ttl "+whisker[0]+"\ttr "+whisker[1])

B = tkinter.Button(top, text ="Print data", command = helloCallBack)

B.pack()
top.mainloop()