import argparse
import sys
import json
import socket
import select

MAX_UDP_PACKET_SIZE = 65507

parser = argparse.ArgumentParser()
parser.add_argument("-sp", type=int)
parser.add_argument("-sip", type=str)
parser.add_argument("-u", type=str)

args = parser.parse_args(sys.argv[1:])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

send_message = {"type": "LIST"}
sign_in_message = {"type": "SIGN-IN", "message": args.u}

while True:

    # Use select method to know when a socket is ready to be read
    ready, ignore, ignore2 = select.select([s], [], [], 0.1)

    for x in ready:
        print x.recv(MAX_UDP_PACKET_SIZE)

    user_input = raw_input("> ")
    if user_input.split()[0] == "list":
        s.sendto(json.dumps(send_message), ("10.0.0.70", 9090))
