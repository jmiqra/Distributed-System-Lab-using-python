import socket               # Import socket module
import sys
import random
from thread import *
import threading



lock1 = threading.Lock()
lock2 = threading.Lock()

flag = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = 	socket.gethostname()		#'192.168.43.133' #socket.gethostname()    # Get local machine name
port = 1235                  # Port for service
s.bind((host, port))           # Bind to the port

s.listen(5)                 # Wait for client connection
							# Accept connection from the client

def func():	               #copy the jokes in an array from file
	file = open('joke.txt', 'r')
	array = []
	for line in file:
		#print line,				#adding a comma doesnt let it go to new line
		array.append(line)
	return array


def iequal(a, b):          #convert all strings in uppercase
	try:
	   return a.upper() == b.upper()
	except AttributeError:
	   return a == b

def knock(c):


	#enter = c.recv(1000)
	global flag					# Variable for beginning and termination of the server
	array = func()
	error = 0                   #initially no error
	yes = 1
	jokes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]    #to check which jokes have been sent
	rand = random.randint(0 , 29)
	jokes[rand]=1           #select a random joke
	i = rand * 6
	count = 1
	#print rand
	while True:
		#print rand , "inside"
		if yes == 1:
			#getnowjoke()
			if error == 0:     #if there is no error
				if (i % 6) == 4:    #and not the first time server send a joke
					c.send(array[i] + array[i+1])
				else:                  #send first joke
					c.send(array[i])
				#i = i+1

			else:     #if there is any error in client's response
				boo = 'You are supposed to say, ' + array[i+1] +  'Lets try again.' + '\n' + 'Server: '		## add ' in lets
				c.send(boo)
				i = rand * 6
				error = 0
				yes = 1
				continue   # if there is an error starts from beginning

			data = c.recv(10000)    #receive response from the client
			temp = data
			data = data + '\n'
			print (array[i+1] , ' ' ,data, ' ', i)

			if iequal(data,array[i+1]):
				print ('correct')
				error = 0
				i = i+2
			else:
				error = 1

			if  (i % 6) >= 4 and iequal(temp,'Y'):   #if the client wants nore jokes
				yes = 1
				print ('yes')
				error = 0				#added now
				if count == 30:     #if all jokes are sent
					print ("I have no more jokes to tell.")
					c.send('I have no more jokes to tell.')
					break
				#getnowjoke()
				#array = func()
				while jokes[rand] == 1:
					rand = random.randint(0 , 29)    #select a random joke
				jokes[rand]=1                        #mark the joke as sent
				i=rand*6
				count+=1
				print ('count ' , count)
			if iequal(temp,'N') and (i % 6) >= 4:   #if the client doesn't want anymore joke
				yes = 0
				print ('no')
				c.send('N')
				#destroy the connection
				break

	c.close() 					# Terminate the connection
	lock1.acquire()             # decrements the counter
	try:
		flag = flag - 1
		print (flag)
	finally:
		lock1.release()          #
	print ("end")
	if flag == 0:
		s.shutdown(socket.SHUT_RDWR)
		s.close()
		return

	#thread.exit()


#main

while 1:
	#wait to accept a connection - blocking call
	try:
		c, addr = s.accept()
	except Exception:
		print ("server closed")
		break
	print ('Got connection from', addr)


	lock1.acquire() # decrements the counter
	try:
		flag = flag + 1
	finally:
		lock1.release()


	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
	try:
		start_new_thread(knock,(c,))
	except Exception:
		pass

	print ('flag is ' , flag)
	if flag == 0:
		break
#s.shutdown(socket.SHUT_RDWR)
s.close()

