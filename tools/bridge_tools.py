from smolagents import tool
import json


def create_bridge_tools(ssh_manager):

    @tool
    def get_interfaces() -> list:
        """
        List all network interfaces on the bridge VM.

        Use this tool when asked to:
        - List or inspect network interfaces.
        - Check whether interfaces are UP or DOWN.
        - Inspect interface properties such as MAC addresses or MTU.

        Returns:
            A list of dictionaries. Each dictionary represents
            one network interface and contains:

            - intrface (str): Interface name, such as eth0, lo, or br0.
            - operstate (str): Operational state, such as UP,
              DOWN, or UNKNOWN.
            - state (str): Interface flags, such as UP,
              LOWER_UP, BROADCAST, or LOOPBACK.
            - mtu (int): Maximum transmission unit.
            - address (str): Interface MAC address.

        Important:
            Use 'interface' for the interface name.
            Use 'state' for the operational state.
            Do not assume keys named 'interface_name' or
            'operational_state' exist.
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
                "mtu": interface.get("mtu"),
                "mac": interface.get("address")
            })            

        return selected_interfaces

    @tool
    def get_bridge_ports() -> list:
        """
        Inspect interfaces attached to Linux bridges.

        Use this tool when asked to:
        - Identify which interfaces belong to a bridge.
        - Determine which ports are attached to br0.
        - Inspect bridge port states.
        - Determine which bridge device manages an interface.

        Returns:
            A list of dictionaries representing bridge port
            membership information. 

            Common fields include:
            - interface (str): Name of the port interface.
            - bridge (str): Name of the bridge master device.
            - state (str): Bridge port state.
            - flags (list[str]): Interface flags.
            - priority (int): Bridge port priority.
            - cost (int): Bridge port path cost.

        Important:
            This tool reports bridge membership and port
            configuration, not general interface information.
            Use get_interfaces() to inspect all interfaces.
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
                "priority": port.get("priority"),
                "cost": port.get("cost")
            })

        return selected_ports

    @tool
    def get_bridge_details() -> list:
        """
        Inspect Linux bridge device configuration.

        Use this tool when asked to:
        - Inspect the configuration of bridge devices.
        - Identify bridge-specific settings.
        - Check bridge properties and configuration flags.
        - Examine STP or other bridge attributes when available.

        Returns:
            A list of dictionaries describing Linux bridge
            devices.

            Common fields may include:
            - ifname (str): Bridge interface name, such as br0.
            - mtu (int): Maximum transmission unit.
            - address (str): Bridge MAC address.
            - linkinfo (dict): Link-specific information.
            - flags (list[str]): Interface flags.

            Additional bridge-specific attributes may be present
            depending on the Linux kernel and iproute2 version.

        Important:
            This tool inspects bridge devices themselves.
            Use get_bridge_ports() to inspect their attached ports.
        """
        result = ssh_manager.run_command(
            "bridge",
            "ip -d -j link show type bridge"
        )

        return json.loads(result["output"])

    @tool
    def get_bridge_fdb() -> list:
        """
        Inspect the Linux bridge Forwarding Database (FDB).

        Use this tool when asked to:
        - Find learned MAC addresses.
        - Determine which bridge port a MAC address is associated with.
        - Investigate MAC address learning.
        - Inspect forwarding database entries.
        - Troubleshoot Layer 2 forwarding.

        Returns:
            A list of dictionaries representing FDB entries.

            Common fields include:
            - mac (str): Learned MAC address.
            - dev (str): Bridge port associated with the MAC address.
            - master (str): Bridge device associated with the entry,
              when present.
            - vlan (int): VLAN identifier, when present.
            - state (str): FDB entry state, when present.
            - flags (list[str]): FDB entry flags, when present.

        Important:
            An FDB entry associates a MAC address with a bridge
            port. It does not necessarily indicate that the
            associated device is currently reachable.
        """
        result = ssh_manager.run_command(
            "bridge",
            "bridge -j fdb show"
        )

        return json.loads(result["output"])

    return [
        get_interfaces,
        get_bridge_ports,
        get_bridge_details,
        get_bridge_fdb
    ]
