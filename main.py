from smolagents import CodeAgent
from smolagents import LiteLLMModel
import os
from smolagents import InferenceClientModel

from ssh.vm_config import VMConfig
from ssh.ssh_manager import SSHManager
from tools.bridge_tools import create_bridge_tools
from tools.host_tools import create_host_tools
from prompts.bridge_prompts import BRIDGE_PROMPTS
from instructions.main_instruction import SYSTEM_PROMPT

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

ssh_manager = SSHManager(configs)

ssh_manager.connect("bridge")
# ssh_manager.connect("host-a")
# ssh_manager.connect("host-b")

bridge_tools = create_bridge_tools(ssh_manager)
# host_a_tools = create_host_tools(ssh_manager, "host-a")
# host_b_tools = create_host_tools(ssh_manager, "host-b")

# all_tools = bridge_tools + host_a_tools + host_b_tools

model = LiteLLMModel(
    model_id="ollama_chat/qwen2.5-coder:3b",
    api_base="http://localhost:11434",
    num_ctx=8192,
    temperature=0.1,
)

agent = CodeAgent(
    tools=bridge_tools,
    model=model,
    instructions=SYSTEM_PROMPT,
    max_steps=8,
    verbosity_level=2
)

def run_prompt_tests(agent):

    for index, prompt in enumerate(BRIDGE_PROMPTS, start=1):

        print("\n" + "=" * 70)
        print(f"TEST {index}/{len(BRIDGE_PROMPTS)}")
        print(f"PROMPT: {prompt}")
        print("=" * 70)

        try:
            result = agent.run(prompt)
            print("\nRESULT:")
            print(result)

        except Exception as e:
            print(f"\nERROR: {e}")

    ssh_manager.disconnect_all()

run_prompt_tests(agent)