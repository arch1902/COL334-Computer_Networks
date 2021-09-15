from socket import *
import threading
import sys

serverPort = 8000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('The server is on !')

clients_send = {}
clients_recv = {}

def check(username):
    for i in range(len(username)):
        if not username[i].isdigit() and not username[i].isalpha():
            return False
    return True

def communicate(connectionSocket, addr):
    message = connectionSocket.recv(1024).decode("ascii")
    temp = message.split()
    if len(temp)==0:
        connectionSocket.close()
        sys.exit()
        return
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
                    if recipient!='ALL':
                        if (recipient not in clients_recv) or (recipient not in clients_send):
                            connectionSocket.send(bytes('ERROR 101 No user registered \n \n',encoding='ascii'))
                            continue

                    msg = ' '.join(temp[4:])
                    if len(msg)!=int(temp[3]):
                        connectionSocket.send(bytes('ERROR 103 Header incomplete\n \n',encoding='ascii'))
                        connectionSocket.close()
                        clients_recv[username].close()
                        del clients_recv[username]
                        del clients_send[username]
                        sys.exit()

                    if recipient == 'ALL':
                        cnt = 0
                        for i in clients_recv:
                            if i==username:
                                continue
                            clients_recv[i].send(bytes('FORWARD '+username+'\n Content-length: '+temp[3]+' \n\n'+msg,encoding='ascii'))
                            message = clients_recv[i].recv(1024).decode("ascii")
                            temp_ = message.split()
                            if temp_[0]=='RECEIVED':
                                cnt += 1
                                sender = temp_[1]
                                clients_send[sender].send(bytes('SEND '+username+'\n \n',encoding='ascii'))
                            elif temp_[1]=='103':
                                #print('ERROR 103 Header Incomplete')
                                connectionSocket.send(bytes('ERROR 103 Header incomplete\n \n',encoding='ascii'))
                                connectionSocket.shutdown(SHUT_RDWR)
                                connectionSocket.close()
                                sys.exit()
                            else:
                                sender = temp_[1]
                                clients_send[sender].send(bytes('ERROR 102 Unable to send\n \n',encoding='ascii'))
                    else:
                        clients_recv[recipient].send(bytes('FORWARD '+username+'\n Content-length: '+temp[3]+' \n\n'+msg,encoding='ascii'))
                        message = clients_recv[recipient].recv(1024).decode("ascii")
                        temp = message.split()
                        if temp[0]=='RECEIVED':
                            sender = temp[1]
                            clients_send[sender].send(bytes('SEND '+username+'\n \n',encoding='ascii'))
                        elif temp[1]=='103':
                            # print('ERROR 103 Header Incomplete')
                            connectionSocket.send(bytes('ERROR 103 Header incomplete\n \n',encoding='ascii'))
                            connectionSocket.shutdown()
                            connectionSocket.close()
                            del clients_recv[username]
                            del clients_send[username]
                        else:
                            sender = temp[1]
                            clients_send[sender].send(bytes('ERROR 102 Unable to send\n \n',encoding='ascii'))

        else:
            connectionSocket.send(bytes('REGISTERED TORECV '+username+'\n \n',encoding='ascii'))
            clients_recv[username] = connectionSocket
            sys.exit()
    else:
        connectionSocket.send(bytes('ERROR 100 Malformed username\n \n',encoding='ascii'))
        connectionSocket.shutdown(SHUT_RDWR)
        connectionSocket.close()
        sys.exit()


while True:
    connectionSocket, addr = serverSocket.accept()
    x = threading.Thread(target=communicate, args=(connectionSocket, addr))
    x.start()
    #connectionSocket.close()




