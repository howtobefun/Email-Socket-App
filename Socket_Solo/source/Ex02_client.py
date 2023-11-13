from socket import *
import os
import time

serverName = '127.0.0.1'
serverPort = 50000


while (True):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    message = input("Type message: ")
    clientSocket.send(message.encode())
    answer = clientSocket.recv(1024).decode("utf-8")
    
    print(answer)
    print()

    clientSocket.close()