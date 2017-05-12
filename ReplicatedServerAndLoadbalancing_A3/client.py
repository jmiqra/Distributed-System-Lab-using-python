import socket              									  # Import socket module
import sys
import time
import random


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname()							  # Get local machine name
port = 12345						  # Port for the service
s.connect((host, port))

while True:
	raw_input('Client: ') 
	for i in range(50):
		rand = random.randint(0 , 100)
		s.send(str(rand))	
	  	data = s.recv(10000)
		print 'Server: ' , data	

s.close()    
