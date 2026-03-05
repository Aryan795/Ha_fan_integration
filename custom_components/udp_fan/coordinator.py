import socket
import threading

from .const import DISCOVERY_PORT

devices = {}


def start_listener(hass):

    def listen():

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to all interfaces to receive UDP broadcast discovery packets from fans
        sock.bind(("0.0.0.0", DISCOVERY_PORT))

        while True:

            data, addr = sock.recvfrom(1024)

            ip = addr[0]

            mac = data.decode(errors="ignore")[:12]

            devices[mac] = ip

    thread = threading.Thread(target=listen, daemon=True)

    thread.start()
