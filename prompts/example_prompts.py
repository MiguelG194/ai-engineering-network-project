BRIDGE_PROMPTS = [
    # Interface inspection
    "List all network interfaces on the bridge VM.",
    "Which network interfaces are currently operational?",
    "Which interfaces are attached to a Linux bridge?",

    # Bridge configuration
    "Which Linux bridges are configured on this VM?",
    "What interfaces are members of br0?",
    "Is Spanning Tree Protocol enabled on the bridge?",
    "Is VLAN filtering enabled?",

    # Understanding configuration
    "What is the purpose of br0 on this VM?",
    "How many physical interfaces are connected to br0?",
    "Does the current bridge configuration appear to be functioning correctly?"
]

HOST_PROMPTS = [
    # Interface inspection
    "List all network interfaces on Host A.",
    "Which network interfaces on Host A are currently operational?",
    "Are there any network interfaces on Host B that are DOWN?",

    # IP configuration
    "What IPv4 addresses are assigned to Host A?",
    "What IPv4 addresses are assigned to Host B?",

    # Routing
    "Show the IPv4 routing table on Host A.",
    "What is the default gateway configured on Host A?",
    "Which network interface does Host B use for its default route?",

    # Neighbor inspection
    "What neighboring devices are listed in Host A's neighbor table?",
    "Does Host B have an ARP entry for Host A?",

    # Interface statistics
    "Are there any packet errors or dropped packets on Host A?",
    "Which interfaces on Host B have recorded packet errors or drops?",

    # Connectivity
    "Can Host A successfully ping Host B?",
    "Can Host B successfully ping Host A?",
]

PROMPTS = {
    "bridge": BRIDGE_PROMPTS,
    "host": HOST_PROMPTS,
}