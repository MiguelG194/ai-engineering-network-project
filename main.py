from smolagents import CodeAgent
from smolagents import LiteLLMModel

from ssh.vm_config import VMConfig
from ssh.ssh_manager import SSHManager
from tools.bridge_tools import create_bridge_tools

configs = {
    "bridge": VMConfig(
        name="bridge",
        host="192.168.56.101",
        username="miguel",
        password="12215Abc*"
    )
}

model = LiteLLMModel(
    model_id="ollama/llama3.2:3b",
    api_base="http://localhost:11434"
)

ssh_manager = SSHManager(configs)

ssh_manager.connect("bridge")

bridge_tools = create_bridge_tools(ssh_manager)

agent = CodeAgent(
    tools=bridge_tools,
    model=model
)

try:
    prompt = input("What would you like to investigate? ")

    response = agent.run(prompt)

    print("\nAgent Response:")
    print(response)

finally:
    ssh_manager.disconnect_all()