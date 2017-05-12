import socket               # Import socket module
import sys
import random
import time
from thread import *
import threading



lock1 = threading.Lock()
lock2 = threading.Lock()

flag = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         	# Create a socket object
host = socket.gethostname() 									# Get local machine name
port = 7777             										# Port for service
s.bind((host, port))        									# Bind to the port

s.listen(5)                 									# Wait for client connection
																# Accept connection from the client
def knock(c):

	while True:
		data = c.recv(10000)

		print type(data)
		temp = int(data,base = 10)
		print "Worker2 Started "
		temp = temp * temp
		temp = str(temp)
		time.sleep(1)
		c.send(temp)
	
	"""	
	c.close() 					# Terminate the connection
	lock1.acquire() # decrements the counte
	try:	
		flag = flag - 1
		print flag	
	finally:
		lock1.release()
	print "end" 
	thread.exit() 
	
	"""   


#main

while 1:
	#wait to accept a connection - blocking call

	c, addr = s.accept()	
	
	print 'Worker ', addr

	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
	try:
		start_new_thread(knock,(c,))
	except Exception:
		pass

	


