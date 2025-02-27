from fastapi import FastAPI, HTTPException, Query, status, Request
from typing import List, Optional, Dict
from pyats_connector.api.device_health_state import (
    health_cpu,
    health_memory,
    health_logging,
)
from pyats_connector.api.interface_config import (
    interface_running_config,
    interfaces_status_and_description,
)
from pyats_connector.api.interface_operations import (
    shut_interface,
    unshut_interface,
)
from pyats_connector.api.interface_state import (
    interfaces_status,
    interface_detailed_status,
    interfaces_information,
    interface_admin_status,
    verify_state_up,
    interface_events,
)
from pyats_connector.api.routing import (
    vrfs_present,
    interface_interfaces_under_vrf,
    route_entries,
)
from pyats_connector.api.isis import (
    isis_neighbors,
    isis_interface_events,
    isis_interfaces,
)
from pyats_connector.inventory import get_devices_from_inventory
from fastapi.responses import JSONResponse

import logging
import functools

from utils.text_utils import get_docstring_summary_and_description

logger = logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file named 'app.log'
        logging.StreamHandler(),  # Also log to the console
    ],
)


def handle_exceptions(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise HTTPException(
                status_code=500, detail="An unexpected error occurred."
            )

    return wrapper


app = FastAPI()


# Add a global exception handler for 5xx errors
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the exception details for debugging
    logger.error(f"Server error: {exc}")

    # Return a generic error message to the user
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected error occurred. Please try again later."
        },
    )


@app.get(
    "/health/memory",
    response_model=Dict,
    summary=get_docstring_summary_and_description(health_memory)[0],
    description=get_docstring_summary_and_description(health_memory)[1],
    operation_id="getHealthMemory",
)
@handle_exceptions
async def get_health_memory(device_name: str = Query(...)):
    return await health_memory(device_name)


@app.get(
    "/health/cpu",
    response_model=Dict,
    summary=get_docstring_summary_and_description(health_cpu)[0],
    description=get_docstring_summary_and_description(health_cpu)[1],
    operation_id="getHealthCpu",
)
@handle_exceptions
async def get_health_cpu(device_name: str = Query(...)):
    return await health_cpu(device_name)


@app.get(
    "/health/logging",
    response_model=Dict,
    summary=get_docstring_summary_and_description(health_logging)[0],
    description=get_docstring_summary_and_description(health_logging)[1],
    operation_id="getHealthLogging",
)
@handle_exceptions
async def get_health_logging(
    device_name: str = Query(...), keywords: Optional[List[str]] = Query(None)
):
    return await health_logging(device_name, keywords)


@app.get(
    "/interface/running-config",
    response_model=Dict,
    summary=get_docstring_summary_and_description(interface_running_config)[0],
    description=get_docstring_summary_and_description(
        interface_running_config
    )[1],
    operation_id="getInterfaceRunningConfig",
)
@handle_exceptions
async def get_interface_running_config(
    device_name: str = Query(...), interface_name: str = Query(...)
):
    return await interface_running_config(device_name, interface_name)


@app.get(
    "/interfaces/status-and-description",
    response_model=Dict,
    summary=get_docstring_summary_and_description(
        interfaces_status_and_description
    )[0],
    description=get_docstring_summary_and_description(
        interfaces_status_and_description
    )[1],
    operation_id="getInterfacesStatusAndDescription",
)
@handle_exceptions
async def get_interfaces_status_and_description(device_name: str = Query(...)):
    return await interfaces_status_and_description(device_name)


@app.get(
    "/interfaces/status",
    response_model=Dict,
    summary=get_docstring_summary_and_description(interfaces_status)[0],
    description=get_docstring_summary_and_description(interfaces_status)[1],
    operation_id="getInterfacesStatus",
)
@handle_exceptions
async def get_interfaces_status(device_name: str = Query(...)):
    return await interfaces_status(device_name)


@app.get(
    "/interface/detailed-status",
    response_model=Dict,
    summary=get_docstring_summary_and_description(interface_detailed_status)[
        0
    ],
    description=get_docstring_summary_and_description(
        interface_detailed_status
    )[1],
    operation_id="getInterfaceDetailedStatus",
)
@handle_exceptions
async def get_interface_detailed_status(
    device_name: str = Query(...), interface_name: str = Query(...)
):
    return await interface_detailed_status(device_name, interface_name)


@app.get(
    "/interface/information",
    response_model=Dict,
    summary=get_docstring_summary_and_description(interfaces_information)[0],
    description=get_docstring_summary_and_description(interfaces_information)[
        1
    ],
    operation_id="getInterfaceInformation",
)
@handle_exceptions
async def get_interface_information(
    request: Request,
    device_name: str = Query(...),
    interfaces_name: Optional[List[str]] = Query(None),
):
    if interfaces_name is None:
        query_params = request.query_params
        interfaces_name = query_params.getlist("interfaces_name")
    return await interfaces_information(device_name, interfaces_name)


@app.get(
    "/interface/admin-status",
    response_model=Dict,
    summary=get_docstring_summary_and_description(interface_admin_status)[0],
    description=get_docstring_summary_and_description(interface_admin_status)[
        1
    ],
    operation_id="getInterfaceAdminStatus",
)
@handle_exceptions
async def get_interface_admin_status(
    device_name: str = Query(...), interface_name: str = Query(...)
):
    return await interface_admin_status(device_name, interface_name)


@app.get(
    "/interface/verify-state-up",
    response_model=Dict,
    summary=get_docstring_summary_and_description(verify_state_up)[0],
    description=get_docstring_summary_and_description(verify_state_up)[1],
    operation_id="verifyInterfaceStateUp",
)
@handle_exceptions
async def verify_interface_state_up(
    device_name: str = Query(...), interface_name: str = Query(...)
):
    return await verify_state_up(device_name, interface_name)


@app.get(
    "/interface/events",
    response_model=Dict,
    summary=get_docstring_summary_and_description(interface_events)[0],
    description=get_docstring_summary_and_description(interface_events)[1],
    operation_id="getInterfaceEvents",
)
@handle_exceptions
async def get_interface_events(
    device_name: str = Query(...), interface_name: str = Query(...)
):
    return await interface_events(device_name, interface_name)


@app.get(
    "/devices/list",
    response_model=List,
    summary=get_docstring_summary_and_description(get_devices_from_inventory)[
        0
    ],
    description=get_docstring_summary_and_description(
        get_devices_from_inventory
    )[1],
    operation_id="getDevicesList",
)
@handle_exceptions
async def get_devices_list_available():
    return await get_devices_from_inventory()


@app.get(
    "/isis/neighbors",
    response_model=Dict,
    summary=get_docstring_summary_and_description(isis_neighbors)[0],
    description=get_docstring_summary_and_description(isis_neighbors)[1],
    operation_id="getIsisNeighbors",
)
@handle_exceptions
async def verify_active_isis_neighbors(device_name: str = Query(...)):
    return await isis_neighbors(device_name)


@app.get(
    "/isis/interface-events",
    response_model=Dict,
    summary=get_docstring_summary_and_description(isis_interface_events)[0],
    description=get_docstring_summary_and_description(isis_interface_events)[
        1
    ],
    operation_id="getIsisInterfaceEvents",
)
@handle_exceptions
async def get_isis_interface_events(device_name: str = Query(...)):
    return await isis_interface_events(device_name)


@app.get(
    "/isis/interface-information",
    response_model=List,
    summary=get_docstring_summary_and_description(isis_interfaces)[0],
    description=get_docstring_summary_and_description(isis_interfaces)[1],
    operation_id="getIsisInterfaceInformation",
)
@handle_exceptions
async def get_isis_interface_information(
    device_name: str = Query(...), vrf_name: str = Query("default")
):
    return await isis_interfaces(device_name, vrf_name)


@app.get(
    "/vrf/present",
    response_model=List,
    summary=get_docstring_summary_and_description(vrfs_present)[0],
    description=get_docstring_summary_and_description(vrfs_present)[1],
    operation_id="getVrfPresent",
)
@handle_exceptions
async def get_vrf_present(device_name: str = Query(...)):
    return await vrfs_present(device_name)


@app.get(
    "/interface/interfaces-under-vrf",
    response_model=List,
    summary=get_docstring_summary_and_description(
        interface_interfaces_under_vrf
    )[0],
    description=get_docstring_summary_and_description(
        interface_interfaces_under_vrf
    )[1],
    operation_id="getInterfacesUnderVrf",
)
@handle_exceptions
async def get_interface_interfaces_under_vrf(
    device_name: str = Query(...), vrf_name: Optional[str] = Query("default")
):
    return await interface_interfaces_under_vrf(device_name, vrf_name)


@app.get(
    "/routing/routes",
    response_model=Dict,
    summary=get_docstring_summary_and_description(route_entries)[0],
    description=get_docstring_summary_and_description(route_entries)[1],
    operation_id="getRoutingRoutes",
)
@handle_exceptions
async def get_routing_routes(
    device_name: str = Query(...),
    vrf_name: Optional[str] = Query(None),
    address_family: str = Query("ipv4"),
):
    return await route_entries(device_name, vrf_name, address_family)


@app.patch(
    "/interface/shut",
    response_model=None,
    summary=get_docstring_summary_and_description(shut_interface)[0],
    description=get_docstring_summary_and_description(shut_interface)[1],
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="shutInterface",
)
@handle_exceptions
async def action_shut_interface(
    device_name: str = Query(...), interface_name: str = Query(...)
):
    await shut_interface(device_name, interface_name)


@app.patch(
    "/interface/unshut",
    response_model=None,
    summary=get_docstring_summary_and_description(unshut_interface)[0],
    description=get_docstring_summary_and_description(unshut_interface)[1],
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="unshutInterface",
)
@handle_exceptions
async def action_unshut_interface(
    device_name: str = Query(...), interface_name: str = Query(...)
):
    await unshut_interface(device_name, interface_name)
