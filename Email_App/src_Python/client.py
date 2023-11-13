import socket

msg = "\r\n Anh DuyTech"
endmsg = "\r\n.\r\n"

recipient = "\"baoduytdn@gmail.com\""
sender = "\"duytdn2806@gmail.com\""
username = "baoduytdn@gmail.com"
password = "password"

# Mail server is host machine + used port when running jar file
mailserver = '127.0.0.1'
SMTP_port = 2225
POP3_port = 3335
clientSocket = socket.socket()
clientSocket.connect((mailserver, SMTP_port))
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
	print('220 reply not received from server.')

heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
	print('250 reply not received from server.')
	
mailFromCommand = f"MAIL FROM: {sender}\r\n"
clientSocket.send(mailFromCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
	print('250 reply not received from server.')
	
rcptToCommand = f"RCPT TO: {recipient}\r\n"
clientSocket.send(rcptToCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
	print('250 reply not received from server.')
	
dataCommand = "DATA\r\n"
clientSocket.send(dataCommand.encode())
recv4 = clientSocket.recv(1024).decode()
if (recv4[:3] == '354'):
    clientSocket.send((msg).encode())
    clientSocket.send((endmsg).encode())

quit_command = "QUIT\r\n"
clientSocket.send(quit_command.encode())

clientSocket.close()

clientSocket = socket.socket()
clientSocket.connect((mailserver, POP3_port))
recv = clientSocket.recv(1024).decode()
print(recv)

userCommand = f"USER {username}\r\n"
clientSocket.send(userCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

passCommand = f"PASS {password}\r\n"
clientSocket.send(passCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

statCommand = "STAT\r\n"
clientSocket.send(statCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

# retrCommand = "RETR 1\r\n"
# clientSocket.send(retrCommand.encode())
# recv = clientSocket.recv(1024).decode()
# print(recv)



