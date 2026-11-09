import json
from pathlib import Path
import os

from smolagents import CodeAgent, LiteLLMModel
from instructions.main_instruction import SYSTEM_PROMPT


def create_agents(all_tools, config_path="models.json"):

    config_path = Path(config_path)

    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    agents = {}

    for model_config in config["models"]:

        name = model_config["name"]
        provider = model_config["provider"]

        if provider == "gemini" and not os.getenv("GEMINI_API_KEY"):
            raise EnvironmentError("GEMINI_API_KEY environment variable not found.")

        settings = {
            key: value
            for key, value in model_config.items()
            if key not in ("name", "provider")
        }

        model = LiteLLMModel(**settings)

        agents[name] = CodeAgent(
            tools=all_tools,
            model=model,
            instructions=SYSTEM_PROMPT,
            max_steps=8,
            verbosity_level=2
        )

    return agents