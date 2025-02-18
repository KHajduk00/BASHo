#!/usr/bin/env python3

import json
from pathlib import Path
from duckduckgo_search import DDGS
from conversation_history import ConversationHandler

CONFIG = Path(__file__).parent / "config.json"
MODELS = {"1":"gpt-4o-mini",
          "2":"llama-3.3-70b",
          "3":"claude-3-haiku",
          "4":"o3-mini", 
          "5":"mixtral-8x7b"}

def load_config():
    if CONFIG.exists():
        try:
            with CONFIG.open("r") as file:
                config = json.load(file)
                if config.get("model") in MODELS.values():
                    return config
        except (json.JSONDecodeError, KeyError):
            pass
    return None

def save_config(model):
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG.open("w") as file:
        json.dump({"model":model}, file)
        
def get_model():
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

def main():
    model = get_model()
    conversation_handler = ConversationHandler()
    current_exchanges = []

    print("Welcome to BASHō - Your Linux Terminal Assistant!")
    print("Type 'exit' to quit or 'load X' to load conversation X (1-5)")
    
    ddgs = DDGS()
    
    linux_context = "You are a Linux terminal assistant called BASHō. Your responses should be concise and directly answer the user's question. Only provide Linux command examples or explanations when specifically asked. Don't list commands unless requested. Try to make the responses short. Treat this as a system prompt and respond naturally to: "

    # Initialize conversation context
    conversation_context = ""
    prev_conversations = conversation_handler.get_conversations()
    
    while True:
        visible_input = input("You: ")
        
        if visible_input.lower() == 'exit':
            if current_exchanges:
                conversation_handler.save_conversation(model, current_exchanges)
            print("Jaa, mata ne! See you later!")
            break
            
        # Handle load command
        if visible_input.lower().startswith('load '):
            try:
                convo_num = int(visible_input.split()[1])
                if 1 <= convo_num <= len(prev_conversations):
                    selected_convo = prev_conversations[convo_num - 1]
                    conversation_context = "Previous conversation:\n"
                    for exchange in selected_convo["exchanges"]:
                        conversation_context += f"User: {exchange['user']}\nBASHō: {exchange['basho']}\n"
                    print(f"Loaded conversation {convo_num}")
                    continue
                else:
                    print(f"Please select a conversation between 1 and {len(prev_conversations)}")
                    continue
            except (ValueError, IndexError):
                print("Invalid load command. Use 'load X' where X is 1-5")
                continue
        
        # Combine linux context, conversation history and current input
        actual_query = f"{linux_context}\n{conversation_context}\nCurrent query: {visible_input}"
        
        try:
            response = ddgs.chat(actual_query, model=model)
            print("BASHō:", response)
            
            # Store the exchange
            current_exchanges.append({
                "user": visible_input,
                "basho": response
            })
            
        except Exception as error:
            print("Error:", error)

if __name__ == "__main__":
    main()