import serial
import struct

class serialComs():

	def __init__(self, port, baudrate, timeout):
		self.ser = serial.Serial(port, baudrate, timeout=timeout)
		
	def write(self, byte):
		self.ser.write(byte)
		
	def writeBytes(self,n,i):
		self.ser.write((i).to_bytes(n,byteorder='little',signed=True))
		
	def writeInt32(self, i):
		self.ser.write((i).to_bytes(4,byteorder='little',signed=True))
		
	def readInt32(self):
		return int.from_bytes(self.ser.read(4), byteorder='little',signed=True)
		
	def readFloat(self):
		return struct.unpack('f', self.ser.read(4))

	def readIntn(self,n):
		return int.from_bytes(self.ser.read(n), byteorder='little',signed=True)
		
	def flushInput(self):
		self.ser.flushInput()
		
	def flushOutput(self):
		self.ser.flushOutput()