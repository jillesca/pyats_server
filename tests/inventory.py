"""
This script is used to test the get_devices_from_inventory function
"""

from pprint import pprint as pp
import asyncio

import setup as setup

from pyats_connector.inventory import (
    get_devices_from_inventory,
)


async def main():
    # Use await to call the async function
    devices = await get_devices_from_inventory()

    # Print the results
    pp(devices)


if __name__ == "__main__":
    # Run the main function using asyncio
    asyncio.run(main())
