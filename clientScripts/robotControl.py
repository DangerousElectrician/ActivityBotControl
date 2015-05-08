import serialComs

class robotControl:

	def __init__(self, port, baudrate, timeout):
		self.com = serialComs.serialComs(port, baudrate, timeout)
		self.ticks = [0,0]
		self.whisker = [0,0]
		self.pos = [0,0,0]

	def reset(self):
		self.com.write(b'p')
		
	def updateSensors(self):	
		self.com.write(b'v')
		self.com.flushInput()
		
		self.pos[0], = self.com.readFloat()
		self.pos[1], = self.com.readFloat()
		self.pos[2], = self.com.readFloat()
		self.ticks[0] = self.com.readInt32()
		self.ticks[1] = self.com.readInt32()
		self.ping = self.com.readInt32()
		self.whisker[0] = self.com.readInt32()
		self.whisker[1] = self.com.readInt32()
		
	def startSensors(self):
		self.com.write(b'0')
		
	def stopSensors(self):
		self.com.write([128])
		
	def startDrive(self):
		self.com.write([129])
		
	def stopDrive(self):
		self.com.write([130])		
		
	def getWhisker(self):
		return self.whisker
		
	def getTicks(self):
		return self.ticks
		
	def getPos(self):
		return self.pos
		
	def getPing(self):
		return self.ping
	
	def getPingcm(self):
		return self.ping/58
	
	def getTheta(self):
		return 0.03071833648393195*(self.ticks[1]-self.ticks[0]) # magic number
		
	def driveSpeed(self,l,r):
		self.com.write(b'h')
		self.com.writeInt32(l)
		self.com.writeInt32(r)
