import socket

def clientPOP3(sender, receipt, serverPOP3, port ,password):
    clientPOP3=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientPOP3.connect((serverPOP3,port))
    recv=clientPOP3.recv(1024).decode()
    print(recv)

    userCheck=f"USER {receipt}\r\n"
    clientPOP3.send(userCheck.encode())
    recv=clientPOP3.recv(1024).decode()
    print(recv)

    passCheck=f"PASS{password}\r\n"
    clientPOP3.send(passCheck.encode())
    recv=clientPOP3.recv(1024).decode()
    print(recv)

    countMail="STAT\r\n"
    clientPOP3.send(countMail.encode())
    recv=clientPOP3.recv(1024).decode()
    print(recv)

    checkRetri="RETR 1\r\n"
    clientPOP3.send(checkRetri.encode())
    recv=clientPOP3.recv(1024).decode()
    print(recv)

    quitPOP3="QUIT\r\n"
    clientPOP3.send(quitPOP3.encode())
    recv=clientPOP3.recv(1024).decode()
    print(recv)

    clientPOP3.close()
