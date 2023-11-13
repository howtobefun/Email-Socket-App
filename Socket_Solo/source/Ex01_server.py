from socket import *

serverPort = 50000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('Server is ready')

connectionSocket, addr = serverSocket.accept()
message = connectionSocket.recv(1024).decode("utf-8")

a, operator, b = message.split(" ")
a, b = int(a), int(b)

match operator:
    case '+':
        ans = a + b
        
    case '-':
        ans = a - b
        
    case '*':
        ans = a * b
    case '/':
        try:
            ans = a / b
        except:
            print("Divisor can't be 0")
            ans = "Infinity"
        
connectionSocket.send(str(ans).encode())
connectionSocket.close()
