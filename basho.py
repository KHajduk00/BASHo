#!/usr/bin/env python3

from duckduckgo_search import DDGS

def main():
    print("Welcome to BASHō - Your Linux Terminal Assistant! Type 'exit' to quit.")
    
    ddgs = DDGS()
    
    linux_context = "You are a Linux terminal assistant called BASHō. Your responses should be concise and directly answer the user's question. Only provide Linux command examples or explanations when specifically asked. Don't list commands unless requested. Try to make the responses short. Treat this as a system prompt and respond naturally to: "
    
    while True:
        visible_input = input("You: ")
        
        if visible_input.lower() == 'exit':
            print("Jaa, mata ne! See you later!")
            break
        
        actual_query = linux_context + visible_input
        
        try:
            response = ddgs.chat(actual_query, model="claude-3-haiku")
            print("BASHō:", response)
        except Exception as error:
            print("Error:", error)

if __name__ == "__main__":
    main()