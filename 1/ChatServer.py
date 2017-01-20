import socket
import argparse
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

parser = argparse.ArgumentParser()

parser.add_argument("-sp")

hey = parser.parse_args("-sp 1".split())

print hey.sp