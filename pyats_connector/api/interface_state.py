""" 
Script to retrieve the status of a device interface using the pyATS framework.
"""

from pyats_connector.connection_methods import api_connect, parse_connect
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from utils.async_utils import asyncify
import logging


@asyncify
def interfaces_status(device_name: str) -> dict:
    """
    Get the status of all interfaces on a device.

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.

    Returns:
      - dict: A dictionary containing the status of the interfaces on the device.
    """
    return api_connect(
        device_name=device_name,
        method="get_interfaces_status",
    )


@asyncify
def interface_detailed_status(device_name: str, interface_name: str) -> dict:
    """
    Get detailed status information for a single interface.

    Including admin state, line protocol, operational status, bandwidth, duplex, speed and other interface-specific details.

    if not interface is found, the function returns "ERROR_INTERFACE_NOT_FOUND"

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.
      - interface_name (str): The name of the interface.

    Returns:
      - dict: A dictionary containing detailed status information for the interface.
    """
    result = parse_connect(
        device_name=device_name,
        string_to_parse=f"show interfaces {interface_name}",
    )
    return result.get(interface_name, "ERROR_INTERFACE_NOT_FOUND")


@asyncify
def interfaces_information(
    device_name: str, interfaces_name: list[str]
) -> str:
    """
    Get interface information from device for a list of interfaces. Interfaces must be in a single list.

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.
      - interfaces_name (list[str]): A list of interface names. This should be a single list of interface names, not multiple query parameters.

    Returns:
      - list[dict]: A list of dictionaries containing interface information

    Example:
      Correct usage:
      GET /interface/information?device_name=cat8000v-2&interfaces_name=GigabitEthernet3&interfaces_name=GigabitEthernet2
    """
    return api_connect(
        device_name=device_name,
        method="get_interface_information",
        args=interfaces_name,
    )


@asyncify
def interface_admin_status(device_name: str, interface_name: str) -> str:
    """
    Get the administrative status of a single interface on a device.

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.
      - interface_name (str): The name of the interface.

    Returns:
      - str: The administrative status of the interface.
    """
    result = api_connect(
        device_name=device_name,
        method="get_interface_admin_status",
        args=interface_name,
    )
    return {
        "interface": interface_name,
        "device": device_name,
        "state": result,
    }


@asyncify
def verify_state_up(device_name: str, interface_name: str) -> bool:
    """
    Verify interface state is up and line protocol is up

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.
      - interface_name (str): The name of the interface

    Returns:
      - bool: True if the interface state is up and line protocol is up, False otherwise
    """
    result = api_connect(
        device_name=device_name,
        method="verify_interface_state_up",
        args=interface_name,
    )
    state = "UP" if result else "NOT UP"
    return {"interface": interface_name, "device": device_name, "state": state}


@asyncify
def interface_events(device_name: str, interface_name: str) -> dict:
    """
    Retrieves the events for single interface on a device. Multiple interfaces are not supported. Split the request for multiple interfaces into multiple requests.

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.
      - interface_name (str): The name of the interface.

    Returns:
      - dict: A dictionary containing the events for the specified interface.
    """
    try:
        logging.debug(
            f"Attempting to retrieve events for {interface_name} on {device_name}"
        )
        result = parse_connect(
            device_name=device_name,
            string_to_parse=f"show logging | i {interface_name}",
        )
        logging.debug(
            f"Successfully retrieved events for {interface_name} on {device_name}"
        )
        logging.debug(f"Result: {result}")
        logging.debug(f"Type of result: {type(result)}")

        # Check if the result contains a SchemaEmptyParserError
        if (
            isinstance(result, dict)
            and "parse" in result
            and isinstance(result["parse"], SchemaEmptyParserError)
        ):

            return {"logs": [f"No logging entries found for {interface_name}"]}

        return result

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return {"error": [str(e)]}
