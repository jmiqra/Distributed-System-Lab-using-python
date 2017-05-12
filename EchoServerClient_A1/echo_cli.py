import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# Creating a TCP socket
server_address = ('localhost', 10000)						# Server host name and port number
print 'Connecting to %s port %s' % server_address
sock.connect(server_address)								# Connecting to the server

try:
	while True: 
		message = raw_input('input: ')						# Taking the input message 
		print 'Sending : "%s"' % message
		sock.send(message)									# Sending the input message
		data = sock.recv(150)								# Receiving the echoed message
		if data == "BEGIN":
			print 'Connection "%s"' % data
		else:
			print 'Received : "%s"' % data

finally:
	print 'Closing socket'
	sock.close()											# Socket close

