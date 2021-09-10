from socket import *

SERVER_NAME = "127.0.0.1"
SERVER_PORT = 3604 

my_sock = socket(AF_INET, SOCK_STREAM)

my_sock.connect((SERVER_NAME, SERVER_PORT))


message = input(">>>")

my_sock.send(message.encode())

byte_array = my_sock.recv()

response = byte_array.decode()

print(response)