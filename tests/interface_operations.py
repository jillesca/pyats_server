"""
This script is used to test interface operations
"""

from pprint import pprint as pp
import asyncio

import setup as setup

from load_test_settings import DEVICE_NAME, INTERFACE_NAME

from pyats_connector.api.interface_operations import (
    shut_interface,
    unshut_interface,
)
from pyats_connector.api.interface_state import interfaces_status


async def main():
    print("\n### Initial status: ###")
    pp(await interfaces_status(device_name=DEVICE_NAME))

    print("\n### Shutting interface: ###")
    pp(
        await shut_interface(
            device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
        )
    )

    print("\n### Status after shutting interface: ###")
    pp(await interfaces_status(device_name=DEVICE_NAME))

    print("\n### Unshutting interface: ###")
    pp(
        await unshut_interface(
            device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
        )
    )

    print("\n### Status after unshutting interface: ###")
    pp(await interfaces_status(device_name=DEVICE_NAME))


if __name__ == "__main__":
    asyncio.run(main())
