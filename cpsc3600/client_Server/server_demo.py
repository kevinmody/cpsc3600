from socket import *

INCOMING_HOSTS = ''
INCOMING_PORT = 3604

print("server started")
server_sock = socket(AF_INET, SOCK_STREAM)

server_sock.bind((INCOMING_HOSTS, INCOMING_PORT))

server_sock.listen(5)

print("server listening")

new_sock, client_addr= server_sock.accept()

byte_array = new_sock.recv()

message =  byte_array.decode()

print(message)

message = message.upper()

new_sock.send(message.encode())