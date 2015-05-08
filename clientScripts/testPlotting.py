from pylab import *
import time
import numpy

ion()

tstart = time.time()               # for profiling
h, = plot([],[])

def update_line(hl, new_datax, new_datay):
	hl.set_xdata(numpy.append(hl.get_xdata(), new_datax))
	hl.set_ydata(numpy.append(hl.get_ydata(), new_datay))
	gca().relim()
	gca().autoscale_view()
	draw()

for i in arange(1,200):
	print(i)
	update_line(h,i,2*i)#.set_ydata(sin(x+i/10.0))  # update the data
		
print( 'FPS:' , 200/(time.time()-tstart))