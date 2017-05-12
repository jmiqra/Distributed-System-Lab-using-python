import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# Creating a TCP socket
server_address = ('localhost', 10000)						# Server host name and port number
print 'Starting on %s port %s' % server_address
sock.bind(server_address)									# Binding the socket to the port
sock.listen(1)												# Listening for connections
print 'Waiting for a connection'
connection, client_address = sock.accept()					# Establishing Connection
while True:
	c = 0
	n = 0
	#print 'Connection ', client_address
	while True:
		data = connection.recv(150)							# Receiving message
		if data == "BEGIN":
			c = 1
		elif data == "END":
			c = 2
		elif data == "CLOSE":
			connection.close()								# Connection close
		if c == 1 and data:									# 'c' for checking if the message is 'BEGIN' or 'END'
			if n == 0:										# 'n' for establishing start connection only once in the process
				print 'Start Connection'
				print 'Connection ', client_address
				n = 1
			print 'Received : "%s"' % data
			print 'Sending message back to the Client'
			connection.send(data)							# Sending the received message data back to the client
		elif c == 2:
			print 'Terminated Connection'
			connection.send('Terminated Connection')		# Indicating the connection termination
			break
		else:
			#print 'Connection ', client_address
			connection.send(' ')
			break	
	print 'No Communication'
