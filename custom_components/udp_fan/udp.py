import socket
import json

from .const import COMMAND_PORT


def send_udp(ip, payload):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = json.dumps(payload).encode()

    sock.sendto(message, (ip, COMMAND_PORT))

    sock.close()
