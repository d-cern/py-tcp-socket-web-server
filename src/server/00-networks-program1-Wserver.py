from socket import *  # import socket module
import sys  # In order to terminate the program
import errno
import os
import re

serverSocket = socket(AF_INET, SOCK_STREAM)

# Error-check cmd line arguments
if len(sys.argv) < 2:
	print("Usage: python3 " + sys.argv[0] + " serverAddr serverPort filename")
	sys.exit()

port = int(sys.argv[1])

# Prepare a server socket
try:
	serverSocket.bind(('', port))
	serverSocket.listen(1)
except herror:
	print('ERROR: invalid port')
	serverSocket.close()
	sys.exit()
except OSError:
	print('ERROR: address is already in use by another process')
	serverSocket.close()
	sys.exit()

while True:
	try:
		# Establish the connection
		print('Ready to serve...')
		(connectionSocket, addr) = serverSocket.accept()
		print('Connection accepted')
	#try:
		msg = connectionSocket.recv(1024)

		dec_msg = msg.decode(encoding='utf-8')

		print(f'Decoded message: \n' + dec_msg)

		# browsers will send ACK that has no data, so trying to get filename will give index OoB
		if dec_msg == '':
			continue

		dec_msg_array = dec_msg.split() #[1]
		filename = dec_msg_array[1][1:]

		print(f'filename = {filename}')

		print('Client request: ' + filename)

		# regex matching to check if filename is stop.xx (case-insensitive)
		if re.match('stop(\..*)?', filename, flags=re.I) is not None:
			connectionSocket.send(b'HTTP/1.1 204 No Content\n\n')
			print('Exiting...')
			connectionSocket.close()
			serverSocket.close()
			sys.exit()

		f = open(filename, 'r', encoding='utf-8')
		outputdata = f.read()
		f.close()

		# Send one HTTP header line into socket
		print('200 - Sending ' + filename + '\n')
		connectionSocket.send(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n')

		# Send the content of the requested file to the client
		i = 0
		while i < len(outputdata): #for i in range(0, len(outputdata)):
			if i+100 >= len(outputdata):
				connectionSocket.send(outputdata[i:].encode(encoding='utf-8'))
			else:
				connectionSocket.send(outputdata[i:i+100].encode(encoding='utf-8'))
			i = i+100

		connectionSocket.send("\r\n".encode(encoding='utf-8'))
		connectionSocket.close()
	except KeyboardInterrupt:
		print('\nExiting...')
		serverSocket.close()
		sys.exit()
	except IOError:
		# Send response message for file not found
		print('404 - File requested not found\n')
		connectionSocket.send(b'HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n'
							  b'<html><body><h1>404 Not Found</body></html>')
		connectionSocket.close()

