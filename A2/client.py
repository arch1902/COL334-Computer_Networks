from socket import *
import threading
import sys

username = sys.argv[1]
serverIP = sys.argv[2]

serverPort = 8000
clientSocket1 = socket(AF_INET, SOCK_STREAM)
clientSocket1.connect((serverIP,serverPort))

clientSocket2 = socket(AF_INET, SOCK_STREAM)
clientSocket2.connect((serverIP,serverPort))

clientSocket1.send(bytes('REGISTER TOSEND '+ username +' \n \n',encoding='ascii'))
message = clientSocket1.recv(1024).decode("ascii")
temp = message.split()


if temp[2]=='Malformed':
    print('Malformed Username !!')
    clientSocket1.close()
    sys.exit()

clientSocket2.send(bytes('REGISTER TORECV '+ username + '\n \n',encoding='ascii'))
message = clientSocket2.recv(1024).decode("ascii")
temp = message.split()

if temp[2]=='Malformed':
    print('Malformed Username !!')
    clientSocket2.close()
    sys.exit()


def read_input():
    print('Thread to read on !!')
    while True:
        input_msg = input()
        if input_msg[0]!='@':
            print('Invalid Format! Please type again.')
            continue
        temp = input_msg.split()
        recipient = temp[0][1:]
        msg = ' '.join(temp[1:])
        clientSocket1.send(bytes('SEND '+recipient+'\n Content-length: '+str(len(msg))+'\n\n '+msg,encoding='ascii'))
        message = clientSocket1.recv(1024).decode("ascii")
        temp = message.split()
        if temp[0]=='SEND':
            print('Message delivered to '+recipient)
        elif temp[1]=='103':
            print('Header Incomplete')
        elif temp[0]=='No':
            print('No such user registered!')
        else:
            print('Unable to send') 
            

def read_forward():
    print('Thread to read incoming msgs on !!')
    while True:
        message = clientSocket2.recv(1024).decode("ascii")
        temp = message.split()
        if temp[0]=='FORWARD':
            sender_username = temp[1]
            if temp[2]=='Content-length:' and temp[3].isdigit():
                clientSocket2.send(bytes('RECEIVED '+sender_username+'\n \n',encoding='ascii'))
                print(sender_username+': ' + ' '.join(temp[4:]))
            else:
                clientSocket2.send(bytes('ERROR 103 Header Incomplete\n \n',encoding='ascii'))
        else:
            continue

x = threading.Thread(target=read_input, args=())
y = threading.Thread(target=read_forward, args=())

####################
x.start()
y.start()

