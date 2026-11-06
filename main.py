from smolagents import CodeAgent
from smolagents import LiteLLMModel
import os
from smolagents import InferenceClientModel

from ssh.vm_config import VMConfig
from ssh.ssh_manager import SSHManager
from tools.bridge_tools import create_bridge_tools
from tools.host_tools import create_host_tools

configs = {
    "bridge": VMConfig(
        name="bridge",
        host="192.168.56.101",
        username="miguel",
        password="12215Abc*"
    ),
    "host-a": VMConfig(
        name="host-a",
        host="placeholder",
        username="placeholder",
        password="12215Abc*"
    ),
    "host-b": VMConfig(
        name="host-b",
        host="placeholder",
        username="placeholder",
        password="12215Abc*"
    )
}

# model = LiteLLMModel(
#     model_id="ollama/llama3.2:3b",
#     api_base="http://localhost:11434"
# )

model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=os.environ["HF_TOKEN"],
    max_tokens=2048,
    temperature=0.1
)

ssh_manager = SSHManager(configs)

ssh_manager.connect("bridge")
# ssh_manager.connect("host-a")
# ssh_manager.connect("host-b")

bridge_tools = create_bridge_tools(ssh_manager)
# host_a_tools = create_host_tools(ssh_manager, "host-a")
# host_b_tools = create_host_tools(ssh_manager, "host-b")

# all_tools = bridge_tools + host_a_tools + host_b_tools

instructions = """
You are a Linux network troubleshooting assistant.

ENVIRONMENT:

You have access to three Linux virtual machines:

1. bridge
   - Acts as a Linux network bridge.
   - Connects host-a and host-b at Layer 2.
   - Provides tools for inspecting bridge interfaces,
     bridge ports, bridge details, and the forwarding database.

2. host-a
   - A Linux host connected to the bridge.
   - Provides tools for inspecting its network configuration
     and testing connectivity.

3. host-b
   - A Linux host connected to the bridge.
   - Provides tools for inspecting its network configuration
     and testing connectivity.

TOOL USAGE:

- Use bridge tools to inspect the Linux bridge.
- Use host-a tools to inspect host-a.
- Use host-b tools to inspect host-b.
- Use ping tools to test connectivity between hosts.
- Use interface, IP address, routing, and neighbor tools
  to investigate network problems.

TROUBLESHOOTING RULES:

- Inspect the actual network configuration.
- Do not assume interface names or IP addresses.
- Diagnose problems before recommending solutions.
- Compare the configurations of both hosts when appropriate.
- Check interface states and IP addresses before testing connectivity.
- Use routing information to determine how traffic should travel.
- Use neighbor information to investigate Layer 2 connectivity.
- Never claim a command succeeded without checking its output.
- Distinguish confirmed problems from possible causes.
- Do not modify network configurations.
- Explain your findings and supporting evidence in your final answer.
"""

agent = CodeAgent(
    tools=bridge_tools,
    model=model,
    instructions=instructions
)

try:
    prompt = "try using the get_interfaces() tool and tell me what you get back."

    response = agent.run(prompt)

    print("\nAgent Response:")
    print(response)

finally:
    ssh_manager.disconnect_all()