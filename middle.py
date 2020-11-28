import random
import socket
import struct
import time

ServerIP = "127.0.0.1"
ClientIP = "127.0.0.1"

ServerPort = 20001
ClientPort = 20002

RecevingPort = 20003

bufferSize = 1024

dropChance = 0.1

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
        message = bytesAddressPair[0]
        if(round(random.uniform(0, 1.0),2) <= dropChance):
            msg = struct.unpack('I I 20s I I', message)
            print('packet ' + str(msg[4]) + ' dropped')
            #if you're wanting it to go through, its
            #message = struct.pack('I I 20s I I', msg[0], msg[1], msg[2], msg[3], msg[4])
            message = struct.pack('I I 20s I I', 0, 0, b'', 0, 0)
        print('sent from server')
        UDPSocket.sendto(message, (ClientIP, ClientPort))
        time.sleep(.5)

    #receves from server
    elif (bytesAddressPair[1][1] == 20002):
        print('Sent from client')
        message = bytesAddressPair[0]
        if(round(random.uniform(0, 1.0),2) <= dropChance):
            msg = struct.unpack('I I 20s I I', message)
            print('packet ' + str(msg[4]) + ' dropped')
            #if you're wanting it to go through, its
            #message = struct.pack('I I 20s I I', msg[0], msg[1], msg[2], msg[3], msg[4])
            message = struct.pack('I I 20s I I', 0, 0, b'', 0, 0)
        time.sleep(.25)
        UDPSocket.sendto(message, (ServerIP, ServerPort))
    else:
        print('wtf?')