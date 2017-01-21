import json
import socket
import argparse
import sys

MAX_PACKET_SIZE = 65507

clients = {}

parser = argparse.ArgumentParser()
parser.add_argument("-sp", type=int)
args = parser.parse_args(sys.argv[1:])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((socket.gethostbyname(socket.gethostname()), args.sp))

print socket.gethostbyname(socket.gethostname())

while True:
    (data, address) = s.recvfrom(MAX_PACKET_SIZE)
    # For future reference: the protocol must be followed exactly
    decoded = json.loads(data)

    if decoded["type"] is "LIST":
        print "Received LIST"
    elif decoded["type"] is "SIGN-ON":
        clients[decoded["message"]] = address
        print "Received SIGN-ON"
    else:
        print "Cannot decode"

