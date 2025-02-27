"""
This script is used to test the device health state operations.
"""

from pprint import pprint as pp
import asyncio

import setup as setup

from load_test_settings import DEVICE_NAME

from pyats_connector.api.device_health_state import (
    health_cpu,
    health_memory,
    health_logging,
)


async def main():
    # Use asyncio.gather to run the async functions concurrently
    cpu_health, memory_health, logging_health = await asyncio.gather(
        health_cpu(device_name=DEVICE_NAME),
        health_memory(device_name=DEVICE_NAME),
        health_logging(device_name=DEVICE_NAME),
    )

    # Print the results
    pp(cpu_health)
    pp(memory_health)
    pp(logging_health)


if __name__ == "__main__":
    # Run the main function using asyncio
    asyncio.run(main())
