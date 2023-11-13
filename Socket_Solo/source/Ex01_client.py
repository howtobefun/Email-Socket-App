from socket import *

serverName = '127.0.0.1'
serverPort = 50000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

a = input('Input a: ')
b = input('Input b: ')
operator = input('Input operator (can be +, -, *, /): ')

message = f"{a} {operator} {b}"

clientSocket.send(message.encode())

ans = clientSocket.recv(1024).decode("utf-8")

print(f'{a} {operator} {b} = {ans}' )
clientSocket.close()