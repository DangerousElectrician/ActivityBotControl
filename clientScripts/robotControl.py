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
		self.com.write([131])
		self.com.flushInput()
		
		self.pos[0], = self.com.readFloat()
		self.pos[1], = self.com.readFloat()
		self.pos[2], = self.com.readFloat()
		self.ticks[0] = self.com.readInt32()
		self.ticks[1] = self.com.readInt32()
		self.ping = self.com.readIntn(2)
		self.whisker = self.com.readIntn(1)
		
	def startSensors(self):
		self.com.write(b'0')
		if (self.com.readInt32() == 42):
			print ("Sensors initialized\n")
		
	def stopSensors(self):
		self.com.write([128])
		
	def startDrive(self):
		self.com.write([129])
		if (self.com.readInt32() == 42):
			print ("Drive System initialized\n")
		
	def stopDrive(self):
		self.com.write([130])		
		
	def startWander(self):
		self.com.write(b'z')
		
	def stopWander(self):
		self.com.write(b'x')
		
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
		self.com.write([132])
		self.com.writeBytes(1,l)
		self.com.writeBytes(1,r)
