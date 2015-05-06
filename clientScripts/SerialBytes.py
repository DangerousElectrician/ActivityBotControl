import serialComs

def main():
	com = serialComs.serialComs('COM6', 9600, timeout=4)
	
	com.write(b'b')
	com.writeInt32(-1000)
	
	#data = b"0aaa000aaaaaaaaa???"
	#com.write(data)
	
	while(True):
		com.write(b'a')
		number = com.readInt32()
		print(number)
		
main()