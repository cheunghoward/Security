import json
import socket
import argparse
import sys

MAX_UDP_PACKET_SIZE = 65507

clients = {}

parser = argparse.ArgumentParser()
parser.add_argument("-sp", type=int)
args = parser.parse_args(sys.argv[1:])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((socket.gethostbyname(socket.gethostname()), args.sp))
print "Server Initialized..."

while True:
    (data, address) = s.recvfrom(MAX_UDP_PACKET_SIZE)
    # For future reference: the protocol must be followed exactly
    decoded = json.loads(data)

    if decoded["type"] == "LIST":
        s.sendto("Signed In Users: " + ", ".join(clients.keys()), address)
    elif decoded["type"] == "SIGN-ON":
        clients[decoded["message"]] = address
    else:
        print "Cannot decode"

