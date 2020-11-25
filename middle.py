import socket
import time

ServerIP = "127.0.0.1"
ClientIP = "127.0.0.1"

ServerPort = 20001
ClientPort = 20002

RecevingPort = 20003

bufferSize = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPSocket.bind((ServerIP, RecevingPort))
print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPSocket.recvfrom(bufferSize)
    print(bytesAddressPair[1][1])    
    #receives from client
    if(bytesAddressPair[1][1] == 20001):
        print('sent from server')
        message = bytesAddressPair[0]
        time.sleep(1)
        UDPSocket.sendto(message, (ClientIP, ClientPort))
    #receves from server
    elif (bytesAddressPair[1][1] == 20002):
        print('Sent from client')
        message = bytesAddressPair[0]
        time.sleep(1)
        UDPSocket.sendto(message, (ServerIP, ServerPort))
    else:
        print('wtf?')