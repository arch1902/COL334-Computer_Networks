from socket import *
import threading
import sys

serverPort = 8000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('The server is ready to receive')

clients_send = {}
clients_recv = {}

def check(username):
    return True

def communicate(connectionSocket, addr):
    message = connectionSocket.recv(1024).decode("ascii")
    temp = message.split()
    username = temp[2]
    if check(username):
        if temp[1]=='TOSEND':
            connectionSocket.send(bytes('REGISTERED TOSEND '+username+'\n \n',encoding='ascii'))
            clients_send[username] = connectionSocket
            while True:
                message = connectionSocket.recv(1024).decode("ascii")
                temp = message.split()
                
                if temp[0]=='SEND':
                    recipient = temp[1]
                    clients_recv[recipient].send(bytes('FORWARD '+username+'\n Content-length: '+temp[3]+' \n\n'+' '.join(temp[4:]),encoding='ascii'))
                    message = clients_recv[recipient].recv(1024).decode("ascii")
                    temp = message.split()
                    print(temp)
                    if temp[0]=='RECEIVED':
                        sender = temp[1]
                        clients_send[sender].send(bytes('SEND '+username+'\n \n',encoding='ascii'))
                    elif temp[1]=='103':
                        #clients[recipient].send(bytes('ERROR 103 Header Incomplete\n \n',encoding='ascii'))
                        print('ERROR 103 Header Incomplete')
                    else:
                        sender = temp[1]
                        clients_send[sender].send(bytes('ERROR 102 Unable to send\n \n',encoding='ascii'))

        else:
            connectionSocket.send(bytes('REGISTERED TORECV '+username+'\n \n',encoding='ascii'))
            clients_recv[username] = connectionSocket
            sys.exit()
    else:
        connectionSocket.send(bytes('ERROR 100 Malformed username\n \n',encoding='ascii'))
        sys.exit()

while True:
    connectionSocket, addr = serverSocket.accept()
    x = threading.Thread(target=communicate, args=(connectionSocket, addr))
    x.start()
    #connectionSocket.close()




