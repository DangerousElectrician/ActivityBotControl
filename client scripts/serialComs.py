import serial

class serialComs():

	def __init__(self, port, baudrate, timeout):
		self.ser = serial.Serial(port, baudrate, timeout=timeout)
		
	def write(self, byte):
		self.ser.write(byte)
		
	def writeInt32(self, i):
		self.ser.write((i).to_bytes(4,byteorder='little',signed=True))
		
	def readInt32(self):
		return int.from_bytes(self.ser.read(4), byteorder='little',signed=True)
		
	def flushInput(self):
		self.ser.flushInput()