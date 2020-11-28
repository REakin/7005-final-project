import socket
import struct
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
f = open('alice.txt', 'rb')
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


def sendpackets(ackedpackets):
    lastSeqAck=0
    count = 0
    while(data):
        for i in ackedpackets:
            if i == lastSeqAck+1:
                lastSeqAck += 1
                print('moving window position')

        if(count<=lastSeqAck+windowSize):
            packet = struct.pack('I I 20s I I', 2, 1, data[count], 3, count)
            UDPSocket.sendto(packet, (localIP, ClientPortR))
            count += 1
            print('Sending packet:'+str(count))

# Sending a reply to client
action_thread = Thread(target=sendpackets, args=(localdata.ackedpackets,))
action_thread.start()
while(True):
    print('ran')
    msgFromServer = UDPSocket.recvfrom(bufferSize)
    msg = struct.unpack('I I 20s I I', msgFromServer[0])
    if msg[0] == 3:
        print(msg[4])
        localdata.ackedpackets.append(msg[4])
        print(localdata.ackedpackets)
