import serialComs

class robotControl:

	def __init__(self, port, baudrate, timeout):
		self.com = serialComs.serialComs(port, baudrate, timeout)

	def updateSensors(self):		
		self.ticks = [0,0]
		self.whisker = [0,0]
		self.com.write(b'v')
		self.com.flushInput()
		self.ticks[0] = self.com.readInt32()
		self.ticks[1] = self.com.readInt32()
		self.ping = self.com.readInt32()
		self.whisker[0] = self.com.readInt32()
		self.whisker[1] = self.com.readInt32()
		
	def getWhisker(self):
		return self.whisker
		
	def getTicks(self):
		return self.ticks
		
	def getPing(self):
		return self.ping
	
	def getTheta(self):
		return 0.03071833648393195*(self.ticks[1]-self.ticks[0]) # magic number
		
	def driveSpeed(self,l,r):
		self.com.write(b'h')
		self.com.writeInt32(l)
		self.com.writeInt32(r)
