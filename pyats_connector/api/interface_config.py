""" 
Script to retrieve the configuration of a device interface using the pyATS framework.
"""

from pyats_connector.connection_methods import api_connect, parse_connect
from utils.async_utils import asyncify


@asyncify
def interface_running_config(device_name: str, interface_name: str) -> dict:
    """
    Get the running config of a single interface on a device.

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.
      - interface_name (str): The name of the interface.

    Returns:
      - dict: The running configuration of the specified interface.
    """
    return api_connect(
        device_name=device_name,
        method="get_interface_running_config",
        args=interface_name,
    )


@asyncify
def interfaces_status_and_description(device_name: str) -> dict:
    """
    Get the status and description of the interfaces per device.

    Args:
      device_name (str): This parameter must come from the REST GET endpoint /devices/list.

    Returns:
      - dict: A dictionary containing the status, protocol, and description of the interfaces.
    """
    result = parse_connect(
        device_name=device_name, string_to_parse="show interfaces description"
    )

    return result.get("interfaces", "ERROR_GETTING_INTERFACES_DESCRIPTION")
