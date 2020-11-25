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
# f = open('newfile.txt', 'w')
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print(struct.unpack('10s', message))
    # clientMsg = "Message from Client:{}".format(message)
    # clientIP = "Client IP Address:{}".format(address)
    # writing = bytes.decode(message)
    # print(bytes.decode(message))
    # print(clientIP)
    # f.write(writing)
    UDPServerSocket.sendto(str.encode(str(count)), (localIP, ServerPortR))
    print('done!') 