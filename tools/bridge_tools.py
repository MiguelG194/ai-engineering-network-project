from smolagents import tool


def create_bridge_tools(ssh_manager):

    @tool
    def get_interfaces() -> str:
        """
        Use this tool when the user asks about network
        interfaces on the bridge VM.

        Returns a list of network interfaces, their operational
        states, MAC addresses, and interface flags.
        """
        result = ssh_manager.run_command(
            "bridge",
            "ip -br link"
        )

        return result["output"]

    @tool
    def get_bridge_ports() -> str:
        """
        Use this tool when the user asks which interfaces are
        attached to Linux bridges or which ports belong to a bridge.

        Returns bridge membership information, including interface
        names, bridge master devices, and port states.

        Use this tool to identify which physical or virtual
        interfaces are connected to br0.
        """
        result = ssh_manager.run_command(
            "bridge",
            "bridge link"
        )

        return result["output"]

    @tool
    def get_bridge_details() -> str:
        """
        Use this tool when the user asks about the configuration
        or properties of Linux bridge devices.

        Returns detailed bridge device information, including
        bridge-specific attributes and configuration flags.
        """
        result = ssh_manager.run_command(
            "bridge",
            "ip -d link show type bridge"
        )

        return result["output"]

    @tool
    def get_bridge_fdb() -> str:
        """
        Use this tool when the user asks about learned MAC addresses,
        forwarding decisions, or the Linux bridge forwarding database.

        Returns forwarding database entries containing learned MAC
        addresses and the associated bridge ports.
        """
        result = ssh_manager.run_command(
            "bridge",
            "bridge fdb show"
        )

        return result["output"]

    return [
        get_interfaces,
        get_bridge_ports,
        get_bridge_details,
        get_bridge_fdb
    ]