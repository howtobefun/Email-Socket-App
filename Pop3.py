import socket

def clientPOP3(sender, receipt, serverPOP3, port ,password):
    clientPOP3=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientPOP3.connect((serverPOP3,port))
    recv1=clientPOP3.recv(1024).decode()
    print(recv1)

    userCheck=f"USER {receipt}\r\n"
    clientPOP3.send(userCheck.encode())
    recv2=clientPOP3.recv(1024).decode()
    print(recv2)

    passCheck=f"PASS{password}\r\n"
    clientPOP3.send(passCheck.encode())
    recv2=clientPOP3.recv(1024).decode()
    print(recv2)

    countMail="STAT\r\n"
    clientPOP3.send(countMail.encode())
    recv2=clientPOP3.recv(1024).decode()
    print(recv2)

    checkRetri="RETR 1\r\n"
    clientPOP3.send(checkRetri.encode())
    recv2=clientPOP3.recv(1024).decode()
    print(recv2)

    quitPOP3="QUIT\r\n"
    clientPOP3.send(quitPOP3.encode())
    recv2=clientPOP3.recv(1024).decode()
    print(recv2)

    clientPOP3.close()
