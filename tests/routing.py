"""
This script is used to test the interface state
"""

from pprint import pprint as pp
import asyncio

import setup as setup

from tests.load_test_settings import DEVICE_NAME

from pyats_connector.api.routing import (
    vrfs_present,
    interface_interfaces_under_vrf,
    route_entries,
)

VRF_DEFAULT = "default"


async def main():
    # Use asyncio.gather to run the async functions concurrently
    vrfs, interfaces_under_vrf, routes = await asyncio.gather(
        vrfs_present(device_name=DEVICE_NAME),
        interface_interfaces_under_vrf(device_name=DEVICE_NAME),
        route_entries(device_name=DEVICE_NAME),
    )

    # Print the results
    pp(vrfs)
    pp(interfaces_under_vrf)
    pp(routes)


if __name__ == "__main__":
    # Run the main function using asyncio
    asyncio.run(main())
