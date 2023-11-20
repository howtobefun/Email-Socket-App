import socket
import base64
from Pop3 import*
def send_email(sender, receipt, name, content, serverSMTP, port):
    
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((serverSMTP,port))
    recv_data=server.recv(1024)
    print(recv_data.decode())
    endmsg = "\r\n.\r\n"

    reply=f'HELO [{serverSMTP}]\r\n'
    server.send(reply.encode())
    recv_data = server.recv(1024)
    print(recv_data.decode())

    reply = f"MAIL FROM: <{sender}>\r\n"
    server.send(reply.encode())
    recv_data = server.recv(1024)
    print(recv_data.decode())

    reply=f"RCPT TO: <{receipt}>\r\n"
    server.send(reply.encode())
    recv_data = server.recv(1024)
    print(recv_data.decode())

    reply="DATA\r\n"
    server.send(reply.encode())
    recv_data = server.recv(1024)
    print(recv_data.decode())

    if (recv_data[:3] == '354'):
        content=content+endmsg
        server.send(content.encode())
        server.recv(1024)

    reply="QUIT\r\n"
    server.send(reply.encode())
    server.recv(1024)

    server.close()


if __name__=="__main__":
    sender="MDV@uwu.com"
    receipt="duywjbu@email.com"
    name="TestSmtp"
    content="Anh iu em nhieu lam"
    serverSMTP="127.0.0.1"
    port=2225
    port2=3335
    password="pass"
    send_email(sender,receipt,name,content,serverSMTP,port)
    clientPOP3(sender,receipt,serverSMTP,port2,password)



