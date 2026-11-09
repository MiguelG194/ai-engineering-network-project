from smolagents import tool
import json


def create_bridge_tools(ssh_manager):

    @tool
    def get_interfaces() -> list:
        """
        Inspect network interfaces on the bridge VM.

        Use this tool when asked to:
        - List network interfaces.
        - Identify interfaces by name (e.g., eth0, lo, br0).
        - Check the operational state of interfaces.
        - Compare the operational states of multiple interfaces.

        Returns:
        A list of dictionaries. Each dictionary represents
        a network interface and contains:

        - interface (str): Interface name.
        - state (str): Operational state, such as UP, DOWN,
        or UNKNOWN.

        Important:
        The state field represents the interface's operational
        state, not its bridge port state.

        This tool does not provide bridge membership information.
        Use get_bridge_ports() to identify interfaces attached
        to Linux bridges.

        Use get_bridge_details() to inspect bridge-specific
        configuration.
        """
        result = ssh_manager.run_command(
            "bridge",
            "ip -j link"
        )

        interfaces = json.loads(result["output"])

        selected_interfaces = []

        for interface in interfaces:
            selected_interfaces.append({
                "interface": interface.get("ifname"),
                "state": interface.get("operstate"),
            })            

        return selected_interfaces

    @tool
    def get_bridge_ports() -> list:
        """
        Inspect interfaces attached to Linux bridges.

        Use this tool when asked to:
        - Identify which interfaces belong to a bridge.
        - Determine which bridge manages a particular interface.
        - Check whether an interface is attached to a bridge.
        - Inspect bridge port states.
        - Investigate bridge port configuration and flags.

        Returns:
        A list of dictionaries. Each dictionary represents
        a bridge port and contains:

        - interface (str): Name of the interface.
        - bridge (str | None): Name of the bridge master device.
        None indicates that no bridge master is reported.
        - state (str): Bridge port state.
        - flags (list[str]): Interface flags associated with the port.

        Important:
        The state field represents the bridge port state,
        not the interface's operational state.

        An interface without a bridge master may be operating
        normally but is not attached to a Linux bridge.

        Use get_interfaces() to inspect general interface
        operational states.

        Use get_bridge_details() to inspect bridge device
        configuration.
        """
        result = ssh_manager.run_command(
            "bridge",
            "bridge -j link"
        )

        ports = json.loads(result["output"])

        selected_ports = []

        for port in ports:
            selected_ports.append({
                "interface": port.get("ifname"),
                "bridge": port.get("master"),
                "state": port.get("state"),
                "flags": port.get("flags"),
            })

        return selected_ports

    @tool
    def get_bridge_details() -> list:
        """
        Inspect Linux bridge device configuration.

        Use this tool when asked to:
        - Identify Linux bridge devices.
        - Inspect bridge-specific settings.
        - Determine whether Spanning Tree Protocol (STP) is enabled.
        - Check whether VLAN filtering is enabled.
        - Inspect a bridge's identifier.

        Returns:
        A list of dictionaries. Each dictionary represents
        a Linux bridge device and contains:

        - interface (str): Bridge interface name, such as br0.
        - stp_enabled (bool): Whether Spanning Tree Protocol
        is enabled.
        - vlan_filtering (int | None): Whether VLAN filtering
        is enabled, when reported by the system.
        - bridge_id (str | None): Bridge identifier, when
        reported by the system.

        Important:
        This tool only returns bridge devices, not individual
        bridge ports.

        A missing vlan_filtering or bridge_id value means
        the corresponding property was not reported.

        Use get_bridge_ports() to inspect attached interfaces
        and their bridge port states.

        Use get_interfaces() to inspect general interface
        operational states.
        """
        
        result = ssh_manager.run_command(
            "bridge",
            "ip -d -j link show type bridge"
        )

        bridges = json.loads(result["output"])

        selected_bridges = []

        for bridge in bridges:
            linkinfo = bridge.get("linkinfo", {})
            info_data = linkinfo.get("info_data", {})

            selected_bridges.append({
                "interface": bridge.get("ifname"),
                "stp_enabled": bool(info_data.get("stp_state", 0)),
                "vlan_filtering": info_data.get("vlan_filtering"),
                "bridge_id": info_data.get("bridge_id")
            })

        return selected_bridges

    return [
        get_interfaces,
        get_bridge_ports,
        get_bridge_details,
    ]
