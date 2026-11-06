
from smolagents import tool


def create_host_tools(ssh_manager, host_name):

    @tool
    def get_interfaces() -> str:
        """
        List all network interfaces on the host VM
        and show their current states.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip -br link"
        )

        return result["output"]

    @tool
    def get_ip_addresses() -> str:
        """
        Display IP addresses assigned to all network
        interfaces on the host VM.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip -br addr"
        )

        return result["output"]

    @tool
    def get_routes() -> str:
        """
        Display the IPv4 routing table of the host VM.
        Shows destination networks, gateways, and interfaces.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip route"
        )

        return result["output"]

    @tool
    def get_default_route() -> str:
        """
        Display the default IPv4 route of the host VM.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip route show default"
        )

        return result["output"]

    @tool
    def get_neighbors() -> str:
        """
        Display the neighbor table of the host VM.
        Shows learned IP-to-MAC address mappings.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip neigh"
        )

        return result["output"]

    @tool
    def get_interface_details() -> str:
        """
        Display detailed network interface statistics.
        Includes received and transmitted packets,
        errors, and dropped packets.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip -s link"
        )

        return result["output"]

    @tool
    def ping_host(destination: str) -> str:
        """
        Test network connectivity to another host.

        Args:
            destination: IPv4 address of the destination host.
        """
        result = ssh_manager.run_command(
            host_name,
            f"ping -4 -c 3 -W 2 {destination}"
        )

        return result["output"]

    return [
        get_interfaces,
        get_ip_addresses,
        get_routes,
        get_default_route,
        get_neighbors,
        get_interface_details,
        ping_host
    ]