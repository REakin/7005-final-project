import socket
import struct
localIP = "127.0.0.1"

ServerPortR = 20003
ServerPortS = 20001

bufferSize = 1024
msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, ServerPortS))

print("UDP server up and listening")
count = 0
# UDPServerSocket.sendto(str.encode(msgFromServer),(localIP, ServerPortR))
# Listen for incoming datagrams

while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = struct.unpack('I I 20s I I', bytesAddressPair[0])
    address = bytesAddressPair[1]

    packet = struct.pack('I I 20s I I', 3, count, b'recived', 3, message[4])
    UDPServerSocket.sendto(packet, (localIP, ServerPortR))
    count += 1
    print('done!')