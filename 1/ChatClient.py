import argparse
import sys
import json
import socket
import select

MAX_UDP_PACKET_SIZE = 65507

# Parse user input
parser = argparse.ArgumentParser()
parser.add_argument("-sip", type=str, required=True)
parser.add_argument("-sp", type=int, required=True)
parser.add_argument("-u", type=str, required=True)
args = parser.parse_args(sys.argv[1:])

SERVER = (args.sip, args.sp)
USERNAME = args.u

# Static message types
list_message = {"type": "LIST"}
sign_in_message = {"type": "SIGN-IN", "message": USERNAME}

# Initialize UDP socket and sign in
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(json.dumps(sign_in_message), SERVER)

while True:

    # Use select method to know when a socket is ready to be read
    ready, ignore, ignore2 = select.select([s], [], [], 0.1)
    user_input_socket, ignore, ignore2 = select.select([sys.stdin], [], [], 0.1)

    for sock in ready:
        print sock.recv(MAX_UDP_PACKET_SIZE)

    if user_input_socket:
        user_input = user_input_socket.recv(MAX_UDP_PACKET_SIZE)
        if user_input.split()[0] == "list":
            s.sendto(json.dumps(list_message), SERVER)
        elif user_input.split()[0] == "send":
            s.sendto(json.dumps({"type": "MESSAGE", "user": user_input.split()[1]}), SERVER)
            # Need to receive message again
            ready, ignore, ignore2 = select.select([s], [], [], 0.1)
            for sock in ready:
                decoded = json.loads(sock.recv(MAX_UDP_PACKET_SIZE))
                print decoded
            s.sendto(" ".join(user_input.split()[2:]), (decoded["host"], decoded["port"]))
