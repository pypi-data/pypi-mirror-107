#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import pickle
import shutil
from tempfile import TemporaryDirectory
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import requests


# Configuration access to Cyber Range endpoint
CORE_API_URL = "http://127.0.0.1:5000"
# Expect a path to CA certs (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CA_CERT_PATH = None
# Expect a path to client cert (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_CERT_PATH = None
# Expect a path to client private key (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_KEY_PATH = None


# Simulation status mapping
map_status = {
    "CREATED": 1,
    "PREPARING": 2,
    "READY": 3,
    "STARTING": 4,
    "PROVISIONING": 5,
    "RUNNING": 6,
    "SCENARIO_PLAYING": 7,
    "STOPPING": 8,
    "DESTROYED": 9,
    "CLONING": 10,
    "PAUSING": 11,
    "UNPAUSING": 12,
    "PAUSED": 13,
    "ERROR": 14,
}


# -------------------------------------------------------------------------- #
# Internal helpers
# -------------------------------------------------------------------------- #


def __get(route: str, **kwargs: Any) -> requests.Response:
    return requests.get(
        f"{CORE_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __post(route: str, **kwargs: Any) -> requests.Response:
    return requests.post(
        f"{CORE_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __put(route: str, **kwargs: Any) -> requests.Response:
    return requests.put(
        f"{CORE_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __delete(route: str, **kwargs: Any) -> requests.Response:
    return requests.delete(
        f"{CORE_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __handle_error(result: requests.Response, context_error_msg: str) -> None:
    if result.headers.get("content-type") == "application/json":
        error_msg = result.json()["message"]
    else:
        error_msg = result.text

    raise Exception(
        f"{context_error_msg}. "
        f"Status code: '{result.status_code}'. "
        f"Error message: '{error_msg}'."
    )


# -------------------------------------------------------------------------- #


def _zip_resources(resources_path: str, temp_dir: str) -> str:
    """Private function to zip resources path content"""
    # get the name of the directory
    dir_name: str = os.path.basename(os.path.normpath(resources_path))
    zip_base_name: str = os.path.join(temp_dir, dir_name)
    zip_format: str = "zip"
    zip_root_dir: str = os.path.dirname(resources_path)
    shutil.make_archive(
        base_name=zip_base_name,
        format=zip_format,
        root_dir=zip_root_dir,
        base_dir=dir_name,
    )
    return "{}.zip".format(zip_base_name)


# -------------------------------------------------------------------------- #


def reset_database() -> Any:
    """Reset the database (clean tables) and
    re-populate it with static info (baseboxes, roles...)
    """
    result = __delete("/database/")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve simulation info from core API")

    return result.json()


def create_simulation(simulation_dict: dict) -> int:
    """Create simulation and return a simulation ID."""

    # hack (turns the python object representation of the network topology
    # into raw bytes)

    # Get the path if one has been provided
    resources_path: str = ""
    if "resources_path" in simulation_dict:
        resources_path = simulation_dict.pop("resources_path", None)

    simulation_dict["network"] = pickle.dumps(simulation_dict["network"]).hex()
    data = json.dumps(simulation_dict)

    # Zipping resource files
    if resources_path != "":
        with TemporaryDirectory() as temp_dir:
            zip_file_name = _zip_resources(resources_path, temp_dir)
            resources_file = open(zip_file_name, "rb")
            files = {"resources_file": resources_file}

            try:
                result = __post(
                    "/simulation/",
                    data=simulation_dict,
                    files=files,
                )
            finally:
                resources_file.close()
    else:
        result = __post(
            "/simulation/",
            data=data,
            headers={"Content-Type": "application/json"},
        )

    if result.status_code != 200:
        __handle_error(result, "Cannot post simulation information to core API")

    id_simulation = result.json()["id"]
    return id_simulation


def get_simulation_status(id_simulation: int) -> str:
    """Return only the status of the simulation"""
    result = __get(f"/simulation/{id_simulation}/status")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve simulation info from core API")

    return result.json()


def fetch_simulation(id_simulation: int) -> dict:
    """Return a simulation dict given a simulation id."""
    result = __get(f"/simulation/{id_simulation}")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve simulation info from core API")

    simulation_dict = result.json()

    # hack (turns the raw bytes representation of the network topology
    # into a real python object)
    b = bytes.fromhex(simulation_dict["network"])
    simulation_dict["network"] = pickle.loads(b)
    return simulation_dict


def fetch_simulations() -> List[Any]:
    """Return all simulations."""
    result = __get("/simulation/")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve simulation info from core API")

    simulation_list = result.json()
    return simulation_list


def execute_operation_simulation(
    id_simulation: int, operation: str, optional_param: Optional[str] = None
) -> int:
    """Execute operation on targeted simulation."""

    uri = f"/simulation/{id_simulation}/{operation}"

    # Handle optional URI parameter
    if optional_param is not None:
        uri = f"{uri}/{str(optional_param)}"

    # Request URI
    result = __get(uri)

    if result.status_code != 200:
        __handle_error(result, "Cannot execute operation '{operation}'")

    # Handle cloning case where a new id_simulation is returned
    if operation == "clone":
        id_simulation = result.json()["id"]

    return id_simulation


def delete_simulation(id_simulation: int) -> Any:
    """Delete a simulation from database."""

    # Delete simulation machines
    delete_machines(id_simulation)

    # Delete simulation
    result = __delete(f"/simulation/{id_simulation}")

    if result.status_code != 200:
        __handle_error(result, "Cannot delete simulation from core API")

    return result.json()


def update_simulation(id_simulation: int, simulation_dict: dict) -> Any:
    """Update simulation information information given a simulation id
    and a dict containing simulation info.
    """
    data = json.dumps(simulation_dict)
    result = __put(
        f"/simulation/{id_simulation}",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    if result.status_code != 200:
        __handle_error(result, "Cannot update simulation information")

    return result.json()


def fetch_simulation_architecture(id_simulation: int) -> Any:
    """Return the architecture of a simulation."""
    result = __get(f"/simulation/{id_simulation}/architecture")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve simulation architecture info")

    return result.json()


def fetch_assets(simulation_id: int) -> Any:
    """Return the list of the assets
    of a given simulation. It corresponds to
    the list of the nodes with some additional
    information.
    """
    result = __get(f"/simulation/{simulation_id}/assets")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve assets from core API")

    return result.json()


def fetch_machine(machine_id: int) -> List[Any]:
    """Return a machine given its id"""
    result = __get(f"/machine/{machine_id}")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve machine from core API")

    return result.json()


def delete_machine(id_machine: int) -> Any:
    """Delete simulation machine given a virtual machine id."""
    # Fetch virtual machine network interfaces
    network_interfaces = fetch_network_interfaces(id_machine)

    # Delete each network interfaces
    for network_interface in network_interfaces:
        delete_network_interface(network_interface["id"])

    # Delete virtual machine
    result = __delete(f"/machine/{id_machine}")

    if result.status_code != 200:
        __handle_error(result, "Cannot delete virtual machine")

    return result.json()


def fetch_machines(id_simulation: int) -> Any:
    """Return simulation virtual machines dict given
    a simulation id, where keys are virtual machine names.
    """
    result = __get(f"/simulation/{id_simulation}/machine")

    if result.status_code != 200:
        __handle_error(
            result, "Cannot retrieve simulation virtual machines from core API"
        )

    return result.json()


def fetch_virtual_machines(id_simulation: int) -> List[dict]:
    """Return simulation virtual machines dict given a simulation id,
    where keys are virtual machine names.
    """
    results = fetch_machines(id_simulation)

    vm_only = filter(lambda m: m["type"] == "virtual_machine", results)
    return list(vm_only)


def fetch_machine_from_name(id_simulation: int, machine_name: str) -> dict:
    """Return simulation machines dict given
    a simulation id, and the name of a machine
    """
    result = __get(f"/simulation/{id_simulation}/machine/{machine_name}")

    if result.status_code != 200:
        __handle_error(
            result, "Cannot retrieve simulation virtual machines from core API"
        )

    return result.json()


def delete_machines(id_simulation: int) -> str:
    """Delete simulation machines given a simulation id."""

    # Fetch simulation machines
    result = __get(f"/simulation/{id_simulation}/machine")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve simulation virtual machines")

    machines_list = result.json()

    # Delete each virtual machine
    for machine in machines_list:
        delete_machine(machine["id"])

    result_json = "{}"
    return result_json


def update_machine(machine_id: int, machine_dict: dict) -> Any:
    """Update  machine information given a  machine id and a dict containing
    machine data.
    """
    data = json.dumps(machine_dict)
    result = __put(
        f"/machine/{machine_id}",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    if result.status_code != 200:
        __handle_error(result, "Cannot update machine information with core API")

    return result.json()


def fetch_network_interfaces(id_machine: int) -> Any:
    """Return network interfaces list given a machine id."""
    result = __get(f"/machine/{id_machine}/network_interface")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve machine network")

    return result.json()


def fetch_network_interface_by_mac(mac_address: str) -> Any:
    """Return network interface list given a mac address."""
    # Fetch virtual machine network interfaces
    result = __get("/network_interface/")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve network interfaces")

    network_interfaces = result.json()

    # Delete each network interfaces
    for network_interface in network_interfaces:
        if network_interface["mac_address"] == mac_address:
            return network_interface
    else:
        return None


def delete_network_interface(id_network_interface: int) -> Any:
    """Delete network interface given an id."""
    result = __delete(f"/network_interface/{id_network_interface}")

    if result.status_code != 200:
        __handle_error(
            result, "Cannot retrieve machine network interfaces from core API"
        )

    return result.json()


def update_network_interface(
    id_network_interface: int, network_interface_dict: dict
) -> Any:
    """Update network interface information information given a network interface id and a
    dict containing network info.

    """
    data = json.dumps(network_interface_dict)
    result = __put(
        f"/network_interface/{id_network_interface}",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    if result.status_code != 200:
        __handle_error(result, "Cannot update network interface information")

    return result.json()


def fetch_baseboxes() -> Any:
    """Return baseboxes list."""
    result = __get("/basebox")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve baseboxes list from core API")

    baseboxes = result.json()
    return baseboxes


def fetch_basebox(id_basebox: int) -> Any:
    """Return basebox given a basebox id."""
    result = __get(f"/basebox/{id_basebox}")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve basebox info from core API")

    basebox = result.json()
    return basebox


def fetch_websites() -> Any:
    """Return websites list."""
    result = __get("/website")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve websites list from core API")

    websites = result.json()
    return websites


def fetch_user_actions() -> Any:
    """Return user actions list."""
    result = __get("/user_action")

    if result.status_code != 200:
        __handle_error(result, "Cannot retrieve user actions list from core API")

    user_actions = result.json()
    return user_actions


def virtclient_status() -> Any:
    """Get virtclient service status."""
    result = __get("/simulation/virtclient_status")

    if result.status_code != 200:
        __handle_error(result, "Cannot get virtclient service status")

    simulation_dict = result.json()
    return simulation_dict


def virtclient_reset() -> Any:
    """Ask to stop virtclient VMs."""
    result = __get("/simulation/virtclient_reset")

    if result.status_code != 200:
        __handle_error(result, "Cannot reset virtclient")

    simulation_dict = result.json()
    return simulation_dict


def tap_simulation(id_simulation: int, iface: str) -> None:
    """Redirect network traffic to the tap interface."""
    result = __get(f"/simulation/{id_simulation}/tap/{iface}")

    if result.status_code != 200:
        __handle_error(
            result, "Cannot activate network traffic redirection from core API"
        )


def untap_simulation(id_simulation: int, iface: str) -> None:
    """Stop redirection of network traffic to the tap interface."""
    result = __get(f"/simulation/{id_simulation}/untap/{iface}")

    if result.status_code != 200:
        __handle_error(result, "Cannot stop network traffic redirection from core API")


def fetch_domains() -> Dict[str, str]:
    """Returns the mapping domain->IP"""

    # FIXME(multi-tenant): we should retrieve domains according to a simulation id
    result = __get("/network_interface/domains")

    if result.status_code != 200:
        __handle_error(result, "Error while fetching domains")

    return result.json()


def snapshot_simulation(simulation_id: int) -> Any:
    """Create a snapshot of a simulation
    All the files will be stored to
    /cyber-range-catalog/simulations/<hash campaign>/<timestamp>/

    Parameters
    ----------
    simulation_id: int
        Simulation to snapshot
    """
    # this API call returns the path where the
    # architecture file will be stored
    result = __post(f"/simulation/{simulation_id}/snapshot")

    if result.status_code != 200:
        __handle_error(result, "Error while creating snapshot")

    return result.json()


def topology_add_websites(
    topology_yaml: str, websites: List[str], switch_name: str
) -> str:
    """Add docker websites node to a given topology, and return the updated topology."""

    data_dict = {
        "topology_yaml": topology_yaml,
        "websites": websites,
        "switch_name": switch_name,
    }
    data = json.dumps(data_dict)
    result = __post(
        "/topology/add_websites",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    if result.status_code != 200:
        __handle_error(result, "Error while adding websites to a topology")

    topology_yaml = result.json()["topology_yaml"]

    return topology_yaml


def topology_add_dga(
    topology_yaml: str,
    algorithm: str,
    switch_name: str,
    number: int,
    resources_dir: str,
) -> Tuple[str, List[str]]:
    """Add docker empty websites with DGA node to a given topology, and return the updated topology
    associated with the domains."""

    data_dict = {
        "topology_yaml": topology_yaml,
        "algorithm": algorithm,
        "switch_name": switch_name,
        "number": number,
        "resources_dir": resources_dir,
    }
    data = json.dumps(data_dict)
    result = __post(
        "/topology/add_dga",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    if result.status_code != 200:
        __handle_error(result, "Error while adding websites to a topology")

    topology_yaml = result.json()["topology_yaml"]
    domains = result.json()["domains"]

    return topology_yaml, domains


def tools_generate_domains(
        algorithm: str,
        number: int,
) -> List[str]:
    """
    Call the backend to generate a list of domains
    :param algorithm: the algorithm for the generation of domains
    :param number: number of domains to generate
    :return: a list of domains
    """
    data_dict = {
        "algorithm": algorithm,
        "number": number,
    }
    data = json.dumps(data_dict)
    result = __post(
        "/domain/generate_domains",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    if result.status_code != 200:
        __handle_error(result, "Error while generating domains")

    domains = result.json()["domains"]

    return domains
