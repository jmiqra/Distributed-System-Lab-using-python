import socket              									  # Import socket module
import sys
import time
from collections import deque
from thread import *
import threading

lock1 = threading.Lock()
lock2 = threading.Lock()
lock3 = threading.Lock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname()							  # Get local machine name
port = 12345						  # Port for the service
s.bind((host, port))
s.listen(5)

#worker socket
w1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
w2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
w3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



workerList = { 0:[0,6666,host],1:[0,7777,host],2:[0,8888,host] }
noOfWorker = 3
now = -1
maxWorkerSlot = 10
#for connecting to the worker
#s1.connect((host, port))

def createconnection(n):
	global workerList
	global w1
	global w2
	global w3
	
	if n == 0:
		w = w1
	if n == 1:
		w = w2
	if n == 2:
		w = w3
	
	worker = workerList[n]
	
	whost = worker[2]
	wport = worker[1]
	print whost , ' ' , wport
	try:
		w.connect((whost,wport))
	except Exception:
		print 'socket error' 
	
	return w

def getworkerconn():
	# need to implement scheduling mechanism here
	"""
	w = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	whost = socket.gethostname()
	wport = 2222
	w.connect((whost,wport))
	
	return w
	"""
	global now 	
	print 'value of now ' , now
	if now >= noOfWorker-1:
		lock3.acquire()
		now = 0
		lock3.release()
	else:
		lock3.acquire()
		now += 1
		lock3.release()
	
	if workerList[now][0] < maxWorkerSlot:
		#now += 1
		lock2.acquire()
		workerList[now][0] += 1			# need to negete 0th index
		lock2.release()
		#print 'aaa'
		conn = createconnection(now)
	else:
		getworkerconn()
		
	print workerList[now]
	return conn
		
		


def acceptClient(c):
	while True:
		#print 'ac client ', 
		msg = c.recv(10000)	
		print 'Number ' , msg
		workerconn = getworkerconn()
		data = worker(workerconn,msg)		
		c.send(data)
		lock2.acquire()
		workerList[now][0] -= 1
		lock2.release()



def worker(workerconn,msg):
	workerconn.send(msg)
	
	squaredval = workerconn.recv(100)
	print 'Squared ' , squaredval 
	return squaredval
	
#def acceptWorker()
	 
countConnection = 0
maxCon = 50 #max con 

queue = deque([])

#main

while 1:
							#wait to accept a connection - blocking call

	##try:
	c, addr = s.accept()
	if countConnection < maxCon:
		lock1.acquire()
		queue.append(c)
		countConnection += 1
		lock1.release()
		print 'data queued ' , queue
		
	
	print countConnection
	lock1.acquire()
	conn = queue.popleft()
	lock1.release()
	##except Exception:
		##print "server tata"	

	print 'Master'

	#try:
	start_new_thread(acceptClient,(conn,))
	#except Exception:
		#pass



   


