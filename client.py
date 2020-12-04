import socket
import struct
import time
import sys
from threading import Thread, Event, local
import yaml

with open("conf.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)


localdata = local()
msgFromClient = b'start'
bytesToSend = struct.pack("I I 20s I I", 1, 1, msgFromClient, 1, 0)

localIP = cfg['client']["connection"]["DestIP"]
ClientPortR = cfg['client']["connection"]['recivingPort']
ClientPortS = cfg['client']["connection"]['sendingPort']

bufferSize = 1024
windowSize = cfg['client']['transfer']['windowSize']

#initialize transfer data
f = open(cfg['client']['transfer']['targetFile'], 'rb')
data = []
l = f.read(20)
while(l):
    data.append(l)
    l = f.read(20)
print(len(data))

# Create a UDP socket at client side
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPSocket.bind((localIP, ClientPortS))
# Send to server using created UDP socket
UDPSocket.sendto(bytesToSend, (localIP, ClientPortR))
localdata.ackedpackets = []
msg = ''


def checktimeout(ackedpackets, count):
    #print('setting timeout period')
    time.sleep(cfg['client']['transfer']['timeoutPeriod'])
    if(count not in ackedpackets):
        print('packet not found resending:'+str(count))
        packet = struct.pack('I I 20s I I', 2, count, data[count], 3, 0)
        UDPSocket.sendto(packet, (localIP, ClientPortR))
        new_Thread = Thread(target=checktimeout, args=(ackedpackets, count,))
        new_Thread.start()

# accedently made the first version full duplex
# def sendPacketsFD(ackedpackets):
#     lastSeqAck=0
#     count = 0
#     while(True):
#         for i in ackedpackets:
#             if i == lastSeqAck+1:
#                 lastSeqAck += 1
#                 print('moving window position')

#         if(count<=lastSeqAck+windowSize):
#             try:
#                 packet = struct.pack('I I 20s I I', 2, count, data[count], windowSize, count)
#                 UDPSocket.sendto(packet, (localIP, ClientPortR))
#                 new_Thread = Thread(target=checktimeout, args=(ackedpackets, count,))
#                 new_Thread.start()
#                 count += 1
#                 print('Sending packet: '+str(count))
#             except(IndexError):
#                 break
#     print('finished')


def sendPacketsHD(ackedpackets):
    lastSeqAck = -1
    count = 0
    window = 0
    x = 0
    while(True):
        for i in ackedpackets:
            if i == lastSeqAck+1:
                lastSeqAck += 1
                window += 1
                #print('moving window position')
        if(window == windowSize or count == 0):
            window = 0
            x=0
            while(x<windowSize):
                try:
                    packet = struct.pack('I I 20s I I', 2, count, data[count], windowSize, 0)
                    UDPSocket.sendto(packet, (localIP, ClientPortR))
                    print('Sending packet: '+str(count))
                    new_Thread = Thread(target=checktimeout, args=(ackedpackets, count,))
                    new_Thread.start()
                    count += 1
                    x += 1
                    print(x)
                except(IndexError):
                    print('sending EOT')
                    time.sleep(1)
                    packet = struct.pack('I I 20s I I', 4, count, b'', windowSize, 0)
                    UDPSocket.sendto(packet, (localIP, ClientPortR))
                    new_Thread = Thread(target=checktimeout, args=(ackedpackets, count,))
                    new_Thread.start()
                    break
                    
    print('finished')


# Sending a reply to client
while(True):
    msgFromServer = UDPSocket.recvfrom(bufferSize)
    msg = struct.unpack('I I 20s I I', msgFromServer[0])
    if msg[0] == 1:
        action_thread = Thread(target=sendPacketsHD, args=(localdata.ackedpackets,))
        action_thread.start()
    if msg[0] == 3:
        localdata.ackedpackets.append(msg[4])
