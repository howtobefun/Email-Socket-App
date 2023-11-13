from socket import *
import time
import os

serverPort = 50000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('Server is ready')

while True: 
    connectionSocket, addr = serverSocket.accept()
    
    message = connectionSocket.recv(1024).decode("utf-8")
    print(f"Incoming message: {message}")

    wordList = message.lower().split(" ")
    answer = "hello, how can i help you"

    if (wordList.__contains__("hello")):
        answer = "hello, how are you?"

    elif (wordList.__contains__("time")):
        curTime = time.localtime()
        answer = f"{curTime.tm_hour}::{curTime.tm_min}::{curTime.tm_sec} {curTime.tm_mday}/{curTime.tm_mon}/{curTime.tm_year}"

    elif (wordList.__contains__("weather")):
        answer = "it is sunny"

    connectionSocket.send(answer.encode())

    print()

    connectionSocket.close()
