#!/usr/bin/env python3
import argparse
import os
import openai

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Chat with an OpenAI model through the terminal."
    )
    parser.add_argument(
        "--model", 
        help="The model to use for the chat (default: gpt-4o).", 
        default="gpt-4o"
    )
    parser.add_argument(
        "--system-prompt", 
        help="An initial system prompt to guide the AI's behavior.", 
        default="You are a helpful assistant."
    )
    return parser.parse_args()

def chat_with_ai(client: openai.Client, model: str, messages: list):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
        return (response.choices[0].message.content or "").strip()
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return None

def main():
    args = parse_arguments()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: The OPENAI_API_KEY environment variable is not set.")
        exit(1)
    
    client = openai.OpenAI(api_key=api_key)

    conversation_history = [{"role": "system", "content": args.system_prompt}]

    print(f"Starting chat with {args.model}. Type 'exit' or 'quit' to end.")
    print("System:", args.system_prompt)
    print("-" * 30)

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting chat.")
                break

            if not user_input.strip():
                continue

            conversation_history.append({"role": "user", "content": user_input})
            
            ai_response = chat_with_ai(client, args.model, conversation_history)

            if ai_response:
                print(f"AI: {ai_response}")
                conversation_history.append({"role": "assistant", "content": ai_response})
            else:
                # If AI response failed, remove the last user message to avoid resending it in a broken state
                conversation_history.pop()


        except KeyboardInterrupt:
            print("\nExiting chat due to interrupt.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    main()
