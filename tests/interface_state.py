"""
This script is used to test the interface state
"""

from pprint import pprint as pp
import asyncio

import setup as setup

from tests.load_test_settings import DEVICE_NAME, INTERFACE_NAME

from pyats_connector.api.interface_state import (
    interfaces_status,
    interface_detailed_status,
    interfaces_information,
    interface_admin_status,
    verify_state_up,
    interface_events,
)

INTERFACES_NAME = ["GigabitEthernet1", "GigabitEthernet2"]


async def main():
    # Use asyncio.gather to run the async functions concurrently
    pp(
        await asyncio.gather(
            interfaces_status(device_name=DEVICE_NAME),
            verify_state_up(
                device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
            ),
            interface_events(
                device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
            ),
        )
    )

    pp(
        await asyncio.gather(
            interface_detailed_status(
                device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
            ),
            interfaces_information(
                device_name=DEVICE_NAME, interfaces_name=INTERFACES_NAME
            ),
            interface_admin_status(
                device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
            ),
        )
    )


if __name__ == "__main__":
    # Run the main function using asyncio
    asyncio.run(main())
