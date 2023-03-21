from socket import *  # import socket module
import sys  # In order to terminate the program
import errno
import os
import re

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a server socket

# Fill in start
try:
	serverSocket.bind(('', 6789))
	serverSocket.listen(1)
except OSError:
	print('ERROR: address is already in use by another process')
	serverSocket.close()
	sys.exit()
# Fill in end

while True:
	try:
		# Establish the connection
		print('Ready to serve...')
		connectionSocket, addr = serverSocket.accept()  # Fill in start 	 #Fill in end
		print('Connection accepted')
	#try:
		message = connectionSocket.recv(1024)  # Fill in start 	 #Fill in end

		filename = message.split()[1]

		print('Client request: ' + filename.decode())

		# regex matching to check if filename is stop.xx (case-insensitive)
		if re.match('/stop(\..*)?', filename.decode(), flags=re.I) is not None:
			connectionSocket.send(b'HTTP/1.1 204 No Content\n\n')
			print('Exiting...')
			connectionSocket.close()
			serverSocket.close()
			sys.exit()

		f = open(filename[1:])
		outputdata = f.read()  # Fill in start #Fill in end


		# Send one HTTP header line into socket
		# Fill in start
		print('200 - Sending ' + filename.decode() + '\n')
		connectionSocket.send(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n')

		# Fill in end
		# Send the content of the requested file to the client
		for i in range(0, len(outputdata)):
			connectionSocket.send(outputdata[i].encode())
		connectionSocket.send("\r\n".encode())
		connectionSocket.close()
	except KeyboardInterrupt:
		print('\nExiting...')
		serverSocket.close()
		sys.exit()
	except IOError:
		# Send response message for file not found
		# Fill in start
		print('404 - File requested not found\n')
		connectionSocket.send(b'HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n'
							  b'<html><body><h1>404 Not Found</body></html>')
		connectionSocket.close()

