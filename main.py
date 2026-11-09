import time
import json
from datetime import datetime

from ssh.vm_config import VMConfig
from ssh.ssh_manager import SSHManager
from tools.bridge_tools import create_bridge_tools
from tools.host_tools import create_host_tools
from models import create_agents
from prompts.example_prompts import PROMPTS

configs = {
    "bridge": VMConfig(
        name="bridge",
        host="192.168.56.101",
        username="miguel",
        password="12215Abc*"
    ),
    "host-a": VMConfig(
        name="host-a",
        host="192.168.56.105",
        username="networklab",
        password="12215Abc*"
    ),
    "host-b": VMConfig(
        name="host-b",
        host="192.168.56.103",
        username="miguel",
        password="12215Abc*"
    )
}

ssh_manager = SSHManager(configs)

ssh_manager.connect("bridge")
ssh_manager.connect("host-a")
ssh_manager.connect("host-b")

bridge_tools = create_bridge_tools(ssh_manager)
host_a_tools = create_host_tools(ssh_manager, "host-a")
host_b_tools = create_host_tools(ssh_manager, "host-b")

all_tools = bridge_tools + host_a_tools + host_b_tools

agents = create_agents(all_tools)

# model = LiteLLMModel(
#     model_id="ollama_chat/qwen2.5-coder:3b",
#     api_base="http://localhost:11434",
#     num_ctx=8192,
#     temperature=0.1,
# )

# agent = CodeAgent(
#     tools=all_tools,
#     model=model,
#     instructions=SYSTEM_PROMPT,
#     max_steps=8,
#     verbosity_level=2
# )

def run_prompt_tests(agents):

    results = []

    try:
        for category, prompts in PROMPTS.items():

            for i, prompt in enumerate(prompts, start=1):

                for agent_name, agent in agents.items():

                    print(f"\n[{category}] Test {i} - {agent_name}")
                    print(f"INPUT: {prompt}")

                    start = time.perf_counter()

                    try:
                        answer = agent.run(prompt)
                        answer = str(answer)

                    except Exception as e:
                        answer = f"ERROR: {e}"

                    elapsed = time.perf_counter() - start

                    print(f"OUTPUT: {answer}")
                    print(f"TIME: {elapsed:.2f} seconds")

                    results.append({
                        "agent": agent_name,
                        "category": category,
                        "test": i,
                        "input": prompt,
                        "output": answer,
                        "time_seconds": round(elapsed, 3)
                    })

    finally:
        ssh_manager.disconnect_all()

    output = {
        "date": datetime.now().isoformat(),
        "total_tests": len(results),
        "agents": list(agents.keys()),
        "results": results
    }

    with open("new_test_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print("\nResults saved to test_results.json")


run_prompt_tests(agents)