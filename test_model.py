from smolagents import LiteLLMModel, CodeAgent, tool

# Mock network state
network_state = {
    "host_a": {
        "interface": "enp0s3",
        "state": "UP",
        "ip": "192.168.1.10/24"
    },
    "host_b": {
        "interface": "enp0s3",
        "state": "UP",
        "ip": "192.168.2.10/24"
    },
    "bridge": {
        "interfaces": ["enp0s9", "enp0s10"]
    }
}


@tool
def get_host_configuration(host: str) -> dict:
    """
    Retrieves the network interface configuration of a host.

    Args:
        host: Name of the host to inspect (host_a or host_b).
    """
    return network_state[host]


@tool
def get_bridge_members() -> list:
    """
    Retrieves the interfaces connected to the Linux bridge.

    Returns:
        A list of interfaces attached to the bridge.
    """
    return network_state["bridge"]["interfaces"]


@tool
def ping_host(source: str, destination: str) -> str:
    """
    Tests connectivity between two hosts.

    Args:
        source: Source host.
        destination: Destination host.
    """
    return "Destination Host Unreachable"


# Initialize model
model = LiteLLMModel(
    model_id="ollama_chat/qwen2.5-coder:3b",
    api_base="http://localhost:11434",
    num_ctx=8192,
    temperature=0.1,
)

# Create a simple agent with no tools
agent = CodeAgent(
    tools=[
        get_host_configuration,
        get_bridge_members,
        ping_host
    ],
    model=model,
    max_steps=8,
)

# Test model
response = agent.run(
    """
    Host A cannot communicate with Host B.

    Investigate the problem using the available tools.
    Determine the likely cause and explain how to fix it.

    Do not modify any configurations.
    """
)

print(response)