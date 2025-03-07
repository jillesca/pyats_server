"""
Script to retrieve the health state of a device using the pyATS framework.
"""

from pyats_connector.connection_methods import api_connect
from utils.async_utils import asyncify


@asyncify
def health_memory(device_name: str) -> dict:
    """
    Retrieves the memory health information for a given device.

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.

    If no memory health issues are detected, the function returns 'No memory health issues detected on the device'.

    Returns:
      - dict: A dictionary containing the memory health information.
    """
    result = api_connect(device_name=device_name, method="health_memory")
    if not result["health_data"]:
        return {"message": "No memory health issues detected on the device"}
    return result


@asyncify
def health_cpu(device_name: str) -> dict:
    """
    Retrieves the CPU health information for a given device.

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.

    If no CPU health issues are detected, the function returns 'No CPU health issues detected on the device'.

    Returns:
      - dict: A dictionary containing the CPU health information.
    """
    result = api_connect(device_name=device_name, method="health_cpu")
    if not result["health_data"]:
        return {"message": "No CPU health issues detected on the device"}
    return result


@asyncify
def health_logging(device_name: str, keywords: list[str] = None) -> dict:
    """
    Retrieves health logging information from a device.

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.
      - keywords (list[str], optional): List of keywords to filter the health logging information.
        Defaults to traceback, error, down and adjchange.

    If no issues are detected, the function returns 'No issues detected on the logs of the device'.

    Returns:
      dict: The health logging information in JSON format.
    """
    if keywords is None:
        keywords = [
            "traceback",
            "Traceback",
            "TRACEBACK",
            "rror",
            "own",
            "ADJCHANGE",
        ]

    result = api_connect(
        device_name=device_name,
        method="health_logging",
        args={"keywords": keywords},
    )

    if not result["health_data"]:
        return {"message": "No issues detected on the logs of the device"}
    return result
