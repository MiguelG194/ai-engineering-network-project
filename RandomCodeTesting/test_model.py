from models import create_agents

agents = create_agents([])

prompt = "Reply with exactly: MODEL_OK"

for name, agent in agents.items():

    print(f"\n{'=' * 50}")
    print(f"MODEL: {name}")
    print('=' * 50)

    try:
        response = agent.run(prompt)
        print(f"OUTPUT:\n{response}")

    except Exception as e:
        print(f"ERROR: {e}")