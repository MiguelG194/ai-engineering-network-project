
from smolagents import tool
import json
import ipaddress


def create_host_tools(ssh_manager, host_name):

    @tool
    def get_interfaces() -> list[dict]:
        """
        List network interfaces and their operational states.
        Use to identify interfaces that are UP or DOWN.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip -j link show"
        )

        data = json.loads(result["output"])
        results = []

        for interface in data:
            results.append({
                "name": interface["ifname"],
                "state": interface["operstate"]
            })

        return results

    @tool
    def get_ip_addresses() -> list[dict]:
        """
        List IP addresses and subnet prefixes assigned to interfaces.
        Use to inspect host IP configuration and compare subnets.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip -j addr show"
        )

        data = json.loads(result["output"])
        results = []

        for interface in data:
            for address in interface.get("addr_info", []):
                if address["family"] == "inet":
                    results.append({
                        "interface": interface["ifname"],
                        "ip": address["local"],
                        "prefix": address["prefixlen"]
                    })

        return results

    @tool
    def get_routes() -> list[dict]:
        """
        List IPv4 routes, their destinations, gateways, and interfaces.
        Use to determine how the host reaches another network.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip -j -4 route show"
        )

        data = json.loads(result["output"])
        results = []

        for route in data:
            results.append({
                "destination": route.get("dst", "default"),
                "gateway": route.get("gateway"),
                "interface": route.get("dev")
            })

        return results

    @tool
    def get_default_route() -> list[dict]:
        """
        Identify the default gateway and outgoing interface.
        Use to determine where traffic to unknown networks is sent.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip -j -4 route show default"
        )

        data = json.loads(result["output"])
        results = []

        for route in data:
            results.append({
                "gateway": route.get("gateway"),
                "interface": route.get("dev")
            })

        return results

    @tool
    def get_neighbors() -> list[dict]:
        """
        Inspect IPv4 neighbor entries.
        Use to identify IP-to-MAC mappings and unusual neighbor states.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip -j -4 neigh show"
        )

        data = json.loads(result["output"])
        results = []

        for neighbor in data:
            results.append({
                "ip": neighbor["dst"],
                "mac": neighbor.get("lladdr"),
                "interface": neighbor.get("dev"),
                "state": neighbor.get("state")
            })

        return results

    @tool
    def get_interface_details() -> list[dict]:
        """
        Inspect interface packet errors and drops.
        Use to identify possible network interface problems.
        """
        result = ssh_manager.run_command(
            host_name,
            "ip -j -s link show"
        )

        data = json.loads(result["output"])
        results = []

        for interface in data:
            stats = interface.get("stats64", interface.get("stats", {}))

            rx = stats.get("rx", {})
            tx = stats.get("tx", {})

            results.append({
                "interface": interface["ifname"],
                "rx_errors": rx.get("errors", 0),
                "rx_dropped": rx.get("dropped", 0),
                "tx_errors": tx.get("errors", 0),
                "tx_dropped": tx.get("dropped", 0)
            })

        return results

    @tool
    def ping_host(destination: str) -> str:
        """
        Test IPv4 connectivity to another host.
        Returns ping results, including packet loss.

        Args:
            destination: IPv4 address of the destination.
        """
        try:
            destination = str(ipaddress.IPv4Address(destination))
        except ipaddress.AddressValueError:
            return "Invalid IPv4 address."

        result = ssh_manager.run_command(
            host_name,
            f"ping -4 -c 3 -W 2 {destination}"
        )

        return result["output"]

    tools = [
        get_interfaces,
        get_ip_addresses,
        get_routes,
        get_default_route,
        get_neighbors,
        get_interface_details,
        ping_host
    ]

    prefix = host_name.replace("-", "_")

    for host_tool in tools:
        host_tool.name = f"{prefix}_{host_tool.name}"

    return tools
