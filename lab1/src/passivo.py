# Server

import socket

HOST = ''
PORT = 5001

def send_data(sock, data):
  sock.send(data)

def receive_data(sock):
	data = sock.recv(1024)
	return data

running = True
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.bind((HOST, PORT))
	sock.listen(1) 

	clientSock, address = sock.accept()
	print(address)

	while running:
		msg_from_client = receive_data(clientSock)
		if not msg_from_client: 
			break
		send_data(clientSock, msg_from_client)