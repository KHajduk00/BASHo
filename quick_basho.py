#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from typing import Dict, Optional
from duckduckgo_search import DDGS

CONFIG = Path(__file__).parent / "config.json"
MODELS: Dict[str, str] = {
    "1": "gpt-4o-mini",
    "2": "llama-3.3-70b",
    "3": "claude-3-haiku",
    "4": "o3-mini",
    "5": "mixtral-8x7b"
}

def load_config() -> Optional[Dict[str, str]]:
    """
    Load configuration from JSON file.
    
    Returns:
        Optional[Dict[str, str]]: Configuration dict if valid, None otherwise
    """
    if CONFIG.exists():
        try:
            with CONFIG.open("r") as file:
                config = json.load(file)
                if config.get("model") in MODELS.values():
                    return config
        except (json.JSONDecodeError, KeyError):
            pass
    return None

def save_config(model: str) -> None:
    """
    Save model configuration to JSON file.
    
    Args:
        model: Name of the model to save
    """
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG.open("w") as file:
        json.dump({"model": model}, file)
        
def get_model() -> str:
    """
    Get the model choice from config or user input.
    
    Returns:
        str: Selected model name
    """
    config = load_config()

    if config:
        return config["model"]

    print("Choose a model: ")
    for key, model in MODELS.items():
        print(f"{key}: {model}")

    while True:
        choice = input("Enter number: ").strip()
        if choice in MODELS:
            save_config(MODELS[choice])
            return MODELS[choice]
        print("Invalid choice, try again.")

def main() -> None:
    """
    Main function that processes a single question and returns BASHō's response.
    Exits with error if no question is provided.
    """
    if len(sys.argv) < 2:
        print("Usage: bsho \"your question here\"")
        sys.exit(1)

    question = sys.argv[1]
    model = get_model()
    linux_context = "You are a Linux terminal assistant called BASHō. Your responses should be very concise and directly answer the user's question. One or two sentences maximum. Only provide Linux command examples or explanations when specifically asked. Don't list commands unless requested. Try to make the responses as short as possible. Answer: "

    try:
        with DDGS() as ddgs:
            response = ddgs.chat(f"{linux_context}{question}", model=model)
            print(f"BASHō: {response}")
    except Exception as error:
        print("Error:", error)

if __name__ == "__main__":
    main()