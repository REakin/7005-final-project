import random
import socket
import struct
import time
import yaml

with open("conf.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)


ServerIP = cfg['middle']['connection']['serverIP']
ClientIP = cfg['middle']['connection']['clientIP']

ServerPort = cfg['middle']['connection']['serverPort']
ClientPort = cfg['middle']['connection']['clientPort']

RecevingPort = cfg['middle']['connection']['recivingPort']

bufferSize = 1024
dropChance = cfg['middle']['transfer']['BER']

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPSocket.bind(("0.0.0.0", RecevingPort))
print("UDP server up and listening")
# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPSocket.recvfrom(bufferSize)
    print(bytesAddressPair[1][1])
    #received from server
    if(bytesAddressPair[1][1] == 20001):
        print('packet recived from server')
        message = bytesAddressPair[0]
        time.sleep(cfg['middle']['transfer']['delay'])
        if(round(random.uniform(0, 1.0), 2) <= dropChance):
            msg = struct.unpack('I I 20s I I', message)
            print('ACK packet ' + str(msg[4]) + ' dropped')
        else:
            UDPSocket.sendto(message, (ClientIP, ClientPort))

    #receved from client
    elif (bytesAddressPair[1][1] == 20002):
        message = bytesAddressPair[0]
        print('packet recived from client')
        time.sleep(cfg['middle']['transfer']['delay'])
        if(round(random.uniform(0, 1.0), 2) <= dropChance):
            msg = struct.unpack('I I 20s I I', message)
            print('DATA packet ' + str(msg[1]) + ' dropped')
        else:
            UDPSocket.sendto(message, (ServerIP, ServerPort))
    else:
        print('error')