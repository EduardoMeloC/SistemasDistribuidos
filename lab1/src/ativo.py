# Client 

import socket

HOST = 'localhost'
PORT = 5001

def send_data(sock, data):
  msg_to_server = data.encode('utf-8')
  sock.send(msg_to_server)

def receive_data(sock):
  msg_from_server = sock.recv(1024)
  string_from_server = msg_from_server.decode('utf-8')
  return string_from_server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  sock.connect((HOST, PORT)) 

  running = True
  while running:
    user_input = input()
    if user_input == 'fim':
      break

    send_data(sock, user_input)
    string_from_server = receive_data(sock)
    print(string_from_server)