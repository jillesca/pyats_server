"""
This script is used to test the interface state
"""

from pprint import pprint as pp
import asyncio

import setup as setup

from pyats_connector.api.isis import (
    isis_neighbors,
    isis_interface_events,
    isis_interfaces,
)

from load_test_settings import DEVICE_NAME

DEVICE_NAME = "cat8000v-2"
VRF = "default"
INTERFACES_NAME = ["GigabitEthernet1", "GigabitEthernet2"]


async def main():
    # Use asyncio.gather to run the async functions concurrently
    pp(
        await asyncio.gather(
            isis_neighbors(device_name=DEVICE_NAME),
            isis_interface_events(device_name=DEVICE_NAME),
            isis_interfaces(device_name=DEVICE_NAME, vrf_name=VRF),
        )
    )


if __name__ == "__main__":
    # Run the main function using asyncio
    asyncio.run(main())
