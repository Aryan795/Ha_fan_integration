import asyncio
import time

from .const import DISCOVERY_PORT

devices = {}


class UDPDiscovery(asyncio.DatagramProtocol):

    def __init__(self, hass):
        self.hass = hass

    def datagram_received(self, data, addr):

        ip = addr[0]
        mac = data.decode(errors="ignore")[:12]

        now = time.time()

        if mac not in devices:

            devices[mac] = {
                "ip": ip,
                "last_seen": now,
                "available": True
            }

            self.hass.async_create_task(
                self.hass.config_entries.flow.async_init(
                    "udp_fan",
                    context={"source": "discovery"},
                    data={"mac": mac, "ip": ip},
                )
            )

        else:

            devices[mac]["last_seen"] = now
            devices[mac]["available"] = True


async def start_discovery(hass):

    loop = asyncio.get_running_loop()

    await loop.create_datagram_endpoint(
        lambda: UDPDiscovery(hass),
        local_addr=("0.0.0.0", DISCOVERY_PORT),
    )
