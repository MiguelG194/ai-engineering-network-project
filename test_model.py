from smolagents import LiteLLMModel, CodeAgent

# Initialize model
model = LiteLLMModel(
    model_id="ollama_chat/llama3.2:3b",
    api_base="http://localhost:11434"
)

# Create a simple agent with no tools
agent = CodeAgent(
    tools=[],
    model=model
)

# Test model
response = agent.run(
    "What is a Linux bridge? Explain in two sentences."
)

print("\nModel response:")
print(response)