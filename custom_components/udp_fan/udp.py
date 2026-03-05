import asyncio
import json

from .const import COMMAND_PORT


async def send_udp(ip, payload):

    loop = asyncio.get_running_loop()

    transport, _ = await loop.create_datagram_endpoint(
        asyncio.DatagramProtocol,
        remote_addr=(ip, COMMAND_PORT),
    )

    message = json.dumps(payload).encode()

    transport.sendto(message)

    transport.close()
