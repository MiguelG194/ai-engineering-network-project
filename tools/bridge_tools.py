from smolagents import tool


def create_bridge_tools(ssh_manager):

    @tool
    def get_interfaces() -> str:
        """
        List all network interfaces on the bridge VM
        and show their current states.
        """
        result = ssh_manager.run_command(
            "bridge",
            "ip -br link"
        )

        return result["output"]

    @tool
    def get_bridge_ports() -> str:
        """
        Identify which network interfaces are connected
        to Linux bridges.
        """
        result = ssh_manager.run_command(
            "bridge",
            "bridge link"
        )

        return result["output"]

    @tool
    def get_bridge_details() -> str:
        """
        Display detailed information about Linux bridge devices.
        """
        result = ssh_manager.run_command(
            "bridge",
            "ip -d link show type bridge"
        )

        return result["output"]

    @tool
    def get_bridge_fdb() -> str:
        """
        Display the forwarding database of the Linux bridge.
        Shows learned MAC addresses and associated ports.
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