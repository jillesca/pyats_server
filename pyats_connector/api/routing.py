""" 
Script to retrieve routing information from a device using the pyATS framework.
"""

from pyats_connector.connection_methods import api_connect
from utils.async_utils import asyncify


@asyncify
def vrfs_present(device_name: str) -> list:
    """
    Get all vrfs from device

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.

    Returns:
      - list: List of vrfs present on the device. If no vrfs are found, returns ["NO_VRFs_FOUND"].
    """
    result = api_connect(
        device_name=device_name,
        method="get_vrf_vrfs",
    )
    if not result:
        return [{"vrf": "NO_VRFs_FOUND", "device": device_name}]
    return [{"vrf": result.keys(), "device": device_name}]


@asyncify
def interface_interfaces_under_vrf(
    device_name: str, vrf_name: str = "default"
) -> list:
    """
    Get interfaces configured under specific Vrf

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.
      - vrf_name (str, optional): Name of the VRF. Defaults to None.

    Returns:
      list: List of interfaces configured under the specified VRF
    """
    result = api_connect(
        device_name=device_name,
        method="get_interface_interfaces_under_vrf",
        args=vrf_name,
    )
    if not result:
        return [
            f"NO_INTERFACES_FOUND_FOR_VRF: {vrf_name} on DEVICE {device_name}"
        ]
    return result


@asyncify
def route_entries(
    device_name: str, vrf_name: str = None, address_family: str = "ipv4"
) -> dict:
    """
    Execute 'show ip route vrf <vrf>' and retrieve the routes.

    Args:
      - device_name (str): This parameter must come from the REST GET endpoint /devices/list.
      - vrf_name (str, optional): The name of the VRF. Defaults to None.
      - address_family (str, optional): The address family name. Defaults to "ipv4".

    TODO: Need to reduce the amount of inrormation returned

    Returns:
      - dict: A dictionary containing the received routes.
    """
    result = api_connect(
        device_name=device_name,
        method="get_routing_routes",
        args={"vrf": vrf_name, "address_family": address_family},
    )
    if not result:
        return {"error": f"NO_ROUTES_FOUND_FOR_VRF_{vrf_name}"}
    return result
