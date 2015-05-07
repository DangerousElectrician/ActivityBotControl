import serialComs

class robotControl:

	def __init__(self, port, baudrate, timeout):
		self.com = serialComs.serialComs(port, baudrate, timeout)

	def reset(self):
		self.com.write(b'p')
		
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
		
	def startSensors(self):
		self.com.write(b'0')
		
	def stopSensors(self):
		self.com.write(b'-')
		
	def startDrive(self):
		self.com.write(b'8')
		
	def stopDrive(self):
		self.com.write(b'9')		
		
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
