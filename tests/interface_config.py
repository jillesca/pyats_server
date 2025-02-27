"""
This script is used to test the interface configuration
"""

from pprint import pprint as pp
import asyncio

import setup as setup

from load_test_settings import DEVICE_NAME, INTERFACE_NAME

from pyats_connector.api.interface_config import (
    interface_running_config,
    interfaces_status_and_description,
)


async def main():
    # Use asyncio.gather to run the async functions concurrently
    running_config, description = await asyncio.gather(
        interface_running_config(
            device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
        ),
        interfaces_status_and_description(device_name=DEVICE_NAME),
    )

    # Print the results
    pp(running_config)
    pp(description)


if __name__ == "__main__":
    # Run the main function using asyncio
    asyncio.run(main())
