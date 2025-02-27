""" 
Script to perform operations on a device interface using the pyATS framework.
"""

from pyats_connector.connection_methods import api_connect
from utils.async_utils import asyncify


@asyncify
def shut_interface(device_name: str, interface_name: str) -> dict:
    """
    Shut down an interface on a device.

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.
      - interface_name (str): The name of the interface to shut down.

    Returns:
      - dict: A dictionary containing the result of the operation.
    """
    return api_connect(
        device_name=device_name,
        method="shut_interface",
        args=interface_name,
    )


@asyncify
def unshut_interface(device_name: str, interface_name: str) -> dict:
    """
    Unshut an interface on a device.

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.
      - interface_name (str): The name of the interface to be unshut.

    Returns:
      dict: A dictionary containing the result of the operation.
    """
    return api_connect(
        device_name=device_name,
        method="unshut_interface",
        args=interface_name,
    )
