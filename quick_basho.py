#!/usr/bin/env python3

import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Union
from duckduckgo_search import DDGS
from conversation_history import ConversationHandler

# Version number for -h flag
VERSION = "0.9.3"

CONFIG = Path(__file__).parent / "config.json"
MODELS: Dict[str, str] = {
    "1": "gpt-4o-mini",
    "2": "llama-3.3-70b",
    "3": "claude-3-haiku",
    "4": "o3-mini",
    "5": "mixtral-8x7b"
}

def load_config() -> Optional[Dict[str, any]]:
    """
    Load configuration from JSON file.
    
    Returns:
        Optional[Dict[str, any]]: Configuration dict if valid, None otherwise
    """
    if CONFIG.exists():
        try:
            with CONFIG.open("r") as file:
                config = json.load(file)
                # Ensure basic structure exists
                if not "search" in config:
                    config["search"] = {}
                if not "video" in config["search"]:
                    config["search"]["video"] = {
                        "max_results": 3,
                        "region": "wt-wt",
                        "safesearch": "moderate"
                    }
                if not "text" in config["search"]:
                    config["search"]["text"] = {
                        "max_results": 5,
                        "region": "wt-wt",
                        "safesearch": "moderate"
                    }
                if not "news" in config["search"]:
                    config["search"]["news"] = {
                        "max_results": 3,
                        "region": "wt-wt",
                        "safesearch": "moderate"
                    }
                if not "editor" in config:
                    config["editor"] = "nano"
                
                # Verify model is valid
                if config.get("model") in MODELS.values():
                    return config
                
        except (json.JSONDecodeError, KeyError):
            pass
    return None

def save_config(model: str, config: Optional[Dict] = None) -> None:
    """
    Save model configuration to JSON file.
    
    Args:
        model: Name of the model to save
        config: Existing config to update (optional)
    """
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    
    if config is None:
        config = {"model": model}
    else:
        config["model"] = model
        
    # Ensure basic structure exists
    if not "search" in config:
        config["search"] = {}
    if not "video" in config["search"]:
        config["search"]["video"] = {
            "max_results": 3,
            "region": "wt-wt",
            "safesearch": "moderate"
        }
    if not "text" in config["search"]:
        config["search"]["text"] = {
            "max_results": 5,
            "region": "wt-wt",
            "safesearch": "moderate"
        }
    if not "news" in config["search"]:
        config["search"]["news"] = {
            "max_results": 3,
            "region": "wt-wt",
            "safesearch": "moderate"
        }
    if not "editor" in config:
        config["editor"] = "nano"
    
    with CONFIG.open("w") as file:
        json.dump(config, file, indent=2)

def edit_config() -> None:
    """
    Open the config file in the user's preferred editor.
    """
    config = load_config()
    if not config:
        # Create default config if it doesn't exist
        save_config(MODELS["1"])
        config = load_config()
    
    editor = config.get("editor", "nano")
    
    try:
        subprocess.run([editor, str(CONFIG)])
        print(f"Configuration updated.")
    except Exception as e:
        print(f"Error opening editor: {e}")
        print(f"You can manually edit the config file at: {CONFIG}")

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

def format_video_result(video: dict) -> str:
    """
    Format result of video search

    Args:
        video: Dictionary containing video info

    Returns:
        str: Fromatted video string
    """
    return (
        f"Title: {video['title']}\n"
        f"Duration: {video['duration']}\n"
        f"URL: {video['content']}\n"
        f"Views: {video['statistics'].get('viewCount', 'N/A')}\n"
    )

def format_text_result(text: dict) -> str:
    """
    Format result of text search

    Args:
        text: Dictionary containing text info

    Returns:
        str: Fromatted text string
    """
    return (
        f"Title: {text['title']}\n"
        f"URL: {text['href']}\n"
        f"Content: {text['body']}\n"
    )

def format_news_result(text: dict) -> str:
    """
    Format result of news search

    Args:
        news: Dictionary containing news info

    Returns:
        str: Fromatted news string
    """
    return (
        f"Title: {text['title']}\n"
        f"Date: {text['date']}\n"
        f"Content: {text['body']}\n"
        f"URL: {text['url']}\n"
        f"Source: {text['source']}\n"
    )

def search_text(query: str) -> None:
    """
    Search for text and show results according to config.

    Args:
        query: Search query string
    """
    config = load_config() or {"search": {}}
    
    # Set defaults if text configuration doesn't exist
    if not "text" in config["search"]:
        config["search"]["text"] = {
            "max_results": 5,
            "region": "wt-wt", 
            "safesearch": "moderate"
        }
        save_config(config.get("model", MODELS["1"]), config)
    
    max_results = config["search"]["text"].get("max_results", 5)
    region = config["search"]["text"].get("region", "wt-wt")
    safesearch = config["search"]["text"].get("safesearch", "moderate")
    
    try:
        with DDGS() as ddgs:
            results = ddgs.text(
                keywords=query,
                region=region,
                safesearch=safesearch,
                max_results=max_results
            )
            if not results:
                print("No text found.")
                return
            
            print(f"\nTop {max_results} Text Results:")
            print("=" * 50)
            for i, text in enumerate(results, 1):
                print(f"\n[Result {i}]")
                print(format_text_result(text))
                
    except Exception as error:
        print("Error searching text:", error)

def search_videos(query: str) -> None:
    """
    Search for videos and show top results according to config.

    Args:
        query: Search query string
    """
    config = load_config() or {"search": {"video": {"max_results": 3, "region": "wt-wt", "safesearch": "moderate"}}}
    max_results = config["search"].get("video", {}).get("max_results", 3)
    region = config["search"].get("video", {}).get("region", "wt-wt")
    safesearch = config["search"].get("video", {}).get("safesearch", "moderate")
    
    try:
        with DDGS() as ddgs:
            results = ddgs.videos(
                keywords=query,
                region=region,
                safesearch=safesearch,
                max_results=max_results
            )
            if not results:
                print("No videos found.")
                return

            print(f"\nTop {max_results} Video Results:")
            print("=" * 50)
            for i, video in enumerate(results, 1):
                print(f"\n[Video {i}]")
                print(format_video_result(video))

    except Exception as error:
        print("Error searching videos:", error)

def search_news(query: str) -> None:
    """
    Search for news and show top 3 results.

    Args:
        query: Search query string
    """
    config = load_config() or {"search": {"news": {"max_results": 3, "region": "wt-wt", "safesearch": "moderate"}}}

    # Set defaults if news configuration doesn't exist
    if not "news" in config["search"]:
        config["search"]["news"] = {
           "max_results": 3,
           "region": "wt-wt",
           "safesearch": "moderate"
        }
        save_config(config.get("model", MODELS["1"]), config)
 
    max_results = config["search"]["news"].get("max_results", 3)
    region = config["search"]["news"].get("region", "wt-wt")
    safesearch = config["search"]["news"].get("safesearch", "moderate")
    
    try:
        with DDGS() as ddgs:
            results = ddgs.news(
                keywords=query,
                region=region,
                safesearch=safesearch,
                max_results=max_results
            )
            if not results:
                print("No news found.")
                return

            print("\nTop {max_results} News Results:")
            print("=" * 50)
            for i, news in enumerate(results, 1):
                print(f"\n[News {i}]")
                print(format_news_result(news))

    except Exception as error:
        print("Error searching news:", error)

def load_conversation(convo_num: int) -> None:
    """
    Load a conversation and start interactive chat mode.
    
    Args:
        convo_num: Number of the conversation to load (1-5)
    """
    conversation_handler = ConversationHandler()
    prev_conversations = conversation_handler.get_conversations()
    
    if not prev_conversations:
        print("No previous conversations found.")
        return
    
    if not 1 <= convo_num <= len(prev_conversations):
        print(f"Please select a conversation between 1 and {len(prev_conversations)}")
        return
    
    selected_convo = prev_conversations[convo_num - 1]
    model = selected_convo["model"]
    current_exchanges = selected_convo["exchanges"].copy()
    
    print(f"Loaded conversation {convo_num} (using model: {model})")
    print("\nPrevious exchanges:")
    for exchange in current_exchanges:
        print(f"You: {exchange['user']}")
        print(f"BASHō: {exchange['basho']}")
    print("\nContinuing conversation... (Type 'exit' to quit)")
    
    conversation_context = "This is a continuation of our previous conversation. Here are our previous exchanges:\n"
    for exchange in current_exchanges:
        conversation_context += f"User: {exchange['user']}\nBASHō: {exchange['basho']}\n"
    conversation_context += "\nNow we're continuing from where we left off. Please respond to: "
    
    linux_context = "You are a Linux terminal assistant called BASHō. Your responses should be concise and directly answer the user's question. Only provide Linux command examples or explanations when specifically asked. Don't list commands unless requested. Try to make the responses short. "
    
    ddgs = DDGS()
    
    while True:
        visible_input = input("\nYou: ")
        
        if visible_input.lower() == 'exit':
            if current_exchanges:
                conversation_handler.save_conversation(model, current_exchanges)
            print("Jaa, mata ne! See you later!")
            break
        
        actual_query = f"{linux_context}\n{conversation_context}{visible_input}"
        
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

def display_help() -> None:
    """
    Display help information including version and available commands.
    """
    print(f"BASHō - Linux Terminal Assistant v{VERSION}")
    print("\nUsage:")
    print("  bsho \"your question here\"            Ask a question to BASHō")
    print("  bsho -v \"your search query\"          Search for videos")
    print("  bsho -t \"your search query\"          Search for text/web results")
    print("  bsho -n \"your news search query\"     Search for news")
    print("  bsho -c<num>                         Continue conversation number <num> (1-5)")
    print("  bsho -dev                            Edit configuration file")
    print("  bsho -h                              Display this help message")
    print("\nAvailable models:")
    for key, model in MODELS.items():
        print(f"  {key}: {model}")
    print("\nBASHō will remember your model preference after the first use.")
    print("Use -dev flag to customize BASHō's behavior.")

def main() -> None:
    """
    Main function that processes a single question and returns BASHō's response.
    Single question can also be a search of videos.
    Single question can also be a search of text.
    Single question can also be a search of news.
    Can continue previous conversations.
    Exits with error if no question is provided.
    """
    if len(sys.argv) < 2:
        print("Usage:")
        print("bsho \"your question here\"")
        print("bsho -v \"your video search here\"")
        print("bsho -t \"your text search here\"")
        print("bsho -n \"your news search here\"")
        print("bsho -c<num> (Load and continue conversation number 1-5)")
        print("bsho -dev (Edit configuration file)")
        print("bsho -h (Display help and version information)")
        sys.exit(1)
    
    # Check if help flag was used
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        display_help()
        return
    
    # Check if dev flag was used
    if sys.argv[1] == "-dev":
        edit_config()
        return
    
    # Check if conversation flag was used (e.g., -c1, -c2, etc.)
    if sys.argv[1].startswith("-c"):
        try:
            convo_num = int(sys.argv[1][2:])
            load_conversation(convo_num)
            return
        except ValueError:
            print("Invalid conversation number. Use -c1 to -c5.")
            sys.exit(1)
    
    # Check if video flag was used
    if sys.argv[1] == "-v":
        if len(sys.argv) < 3:
            print("Please provide a search query after -v flag")
            sys.exit(1)
        search_videos(sys.argv[2])
        return

    # Check if text flag was used
    if sys.argv[1] == "-t":
        if len(sys.argv) < 3:
            print("Please provide a search query after -t flag")
            sys.exit(1)
        search_text(sys.argv[2])
        return

    # Check if news flag was used
    if sys.argv[1] == "-n":
        if len(sys.argv) < 3:
            print("Please provide a search query after -n flag")
            sys.exit(1)
        search_news(sys.argv[2])
        return

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
