import socket
import struct

msgFromClient = b'Hello UDP Server'
bytesToSend = struct.pack("10s",msgFromClient)

localIP = "127.0.0.1"

ClientPortR = 20003
ClientPortS = 20002

bufferSize = 1024

# Create a UDP socket at client side
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPSocket.bind((localIP, ClientPortS))

# Send to server using created UDP socket
UDPSocket.sendto(bytesToSend, (localIP, ClientPortR))

count = 0
msg = ''

# Sending a reply to client
f = open('alice.txt', 'rb')

while(True):
    msgFromServer = UDPSocket.recvfrom(bufferSize)
    if msg != msgFromServer[0]:
        msg = msgFromServer
        print(msg)
        count += 1
        print(count)
        l = f.read(10)
        l = struct.pack('10s',l)
        UDPSocket.sendto(l, (localIP, ClientPortR))