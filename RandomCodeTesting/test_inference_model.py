from smolagents import InferenceClientModel
import os

model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=os.environ["HF_TOKEN"],
    max_tokens=512
)

response = model(
    messages=[
        {
            "role": "user",
            "content": "Write Python code that prints hello world."
        }
    ]
)

print(response)