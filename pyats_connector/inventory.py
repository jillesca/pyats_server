""" 
Script to retrieve the devices from the inventory using the pyATS framework.
"""

from pyats.topology import loader
from utils.async_utils import asyncify
from config.global_settings import TESTBED_FILE


@asyncify
def get_devices_from_inventory() -> list:
    """
    Retrieves a list of existing devices.

    Args:
      - None. The function will always return a list of device names. It doesn't require any arguments.

    Returns:
      - list: A list of device names.
    """
    topology = loader.load(TESTBED_FILE)
    return list(topology.devices.names)
