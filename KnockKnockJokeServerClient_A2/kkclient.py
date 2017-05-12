import socket              									  # Import socket module
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() 								  # Get local machine name
port = 1235        								  # Port for the service
s.connect((host, port))

while True:
	
	data = s.recv(10000)			# data received from the server
	if data == 'N':
		break
	print( "Server: " , data ,)
	if data == 'I have no more jokes to tell.':
		break
	
	msg = raw_input('Client: ') 
	
	s.send(msg)								# send input data to the server
	
s.close()                     						# Close the socket when done
