import socket
import struct
import time
from threading import Thread, Event, local
localdata = local()
msgFromClient = b'Hello UDP Server'
bytesToSend = struct.pack("I I 20s I I", 1, 1, msgFromClient, 1, 0)

localIP = "127.0.0.1"

ClientPortR = 20003
ClientPortS = 20002

bufferSize = 1024
windowSize = 3

#initialize transfer data
f = open('DTRH.txt', 'rb')
data = []
l = f.read(20)
while(l):
    data.append(l)
    l = f.read(20)
print(len(data))
print(data[100])

# Create a UDP socket at client side
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPSocket.bind((localIP, ClientPortS))
# Send to server using created UDP socket
UDPSocket.sendto(bytesToSend, (localIP, ClientPortR))
localdata.ackedpackets = []
msg = ''


def checktimeout(ackedpackets, count):
    print('setting timeout period')
    time.sleep(5)
    if(count not in ackedpackets):
        print('packet not found resending:'+str(count))
        packet = struct.pack('I I 20s I I', 2, 1, data[count], 3, count)
        UDPSocket.sendto(packet, (localIP, ClientPortR))
        new_Thread = Thread(target=checktimeout, args=(ackedpackets, count,))
        new_Thread.start()
    else:
        print('packet acked: '+str(count))


def sendPackets(ackedpackets):
    lastSeqAck=0
    count = 0
    while(True):
        for i in ackedpackets:
            if i == lastSeqAck+1:
                lastSeqAck += 1
                print('moving window position')

        if(count<=lastSeqAck+windowSize):
            try:
                packet = struct.pack('I I 20s I I', 2, 1, data[count], 3, count)
                UDPSocket.sendto(packet, (localIP, ClientPortR))
                new_Thread = Thread(target=checktimeout, args=(ackedpackets, count,))
                new_Thread.start()
                count += 1
                print('Sending packet: '+str(count))
            except(IndexError):
                break
    print('finished')


# Sending a reply to client
action_thread = Thread(target=sendPackets, args=(localdata.ackedpackets,))
action_thread.start()
while(True):
    print('ran')
    msgFromServer = UDPSocket.recvfrom(bufferSize)
    msg = struct.unpack('I I 20s I I', msgFromServer[0])
    if msg[0] == 3:
        print(msg[4])
        localdata.ackedpackets.append(msg[4])
        print(localdata.ackedpackets)
