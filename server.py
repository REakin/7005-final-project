import socket
import struct
import yaml

with open("conf.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

localIP = cfg['server']['connection']['DestIP']

ServerPortR = cfg['server']['connection']['recivingPort']
ServerPortS = cfg['server']['connection']['sendingPort']

bufferSize = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind(("0.0.0.0", ServerPortS))

print("UDP server up and listening")
count = 0
# UDPServerSocket.sendto(str.encode(msgFromServer),(localIP, ServerPortR))
# Listen for incoming datagrams

while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = struct.unpack('I I 20s I I', bytesAddressPair[0])
    address = bytesAddressPair[1]
    if(message[0]==1):
        print('syn packet recived')
        windowSize = message[3]
        packet = struct.pack('I I 20s I I', 1, count, b'recived', 3, 0)
        UDPServerSocket.sendto(packet, (localIP, ServerPortR))
    if(message[0]==2):
        print('data packet recived: seqnum '+str(message[1]))
        packet = struct.pack('I I 20s I I', 3, message[1], b'recived', 3, message[1])
        UDPServerSocket.sendto(packet, (localIP, ServerPortR))
        count += 1
    if(message[0]==4):
        print('EOT packet recived: seqnum '+str(message[1]))
        packet = struct.pack('I I 20s I I', 3, message[1], b'recived', 3, message[1])
        UDPServerSocket.sendto(packet, (localIP, ServerPortR))
  


    # print('Packet Recived: '+str(message[4]))
