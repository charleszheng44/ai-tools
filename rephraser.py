#!/usr/bin/env python3
import argparse
import os
import openai
import subprocess
import readline

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Rephrase a sentence using OpenAI's gpt-3.5-turbo with a specified tone."
    )
    parser.add_argument("sentence", nargs="?", help="The sentence you want to rephrase.")
    parser.add_argument("--model", help="The model to use for rephrasing (default: gpt-4o).", default="gpt-4o")
    parser.add_argument("--prompt", help="The prompt to use for rephrasing.", default="")
    parser.add_argument("--interactive", "-i", action="store_true", help="Enable interactive mode with keyboard shortcuts.")
    
    # Create a mutually exclusive group without the 'required' flag.
    tone_group = parser.add_mutually_exclusive_group()
    tone_group.add_argument(
        "--neutral", action="store_true", help="Rephrase the sentence in a neutral tone (default)."
    )
    tone_group.add_argument(
        "--polite", action="store_true", help="Rephrase the sentence in a polite tone."
    )
    tone_group.add_argument(
        "--casual", action="store_true", help="Rephrase the sentence in a casual tone."
    )
    
    return parser.parse_args()

def determine_tone(args):
    if args.neutral:
        return "neutral"
    elif args.polite:
        return "polite"
    elif args.casual:
        return "casual"
    else:
        # This should not occur because one option is required.
        return "neutral"

def rephrase_sentence(sentence: str, tone: str, client: openai.Client, model: str, prompt: str) -> str:
    # Build the conversation messages for ChatCompletion
    system_message = "You are a helpful assistant that rephrases text."
    user_prompt = f"Rephrase the following sentence in a {tone} tone without including any quotes:\n\n\"{sentence}\""
    if prompt != "":
        user_prompt = f"{prompt}\n\n{user_prompt}"

    response = client.chat.completions.create(model=model,
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.7)

    # Extract and return the rephrased sentence.
    return (response.choices[0].message.content or "").strip()

def interactive_mode(client: openai.Client, model: str, prompt: str):
    print("Interactive Rephraser Mode")
    print("Keyboard shortcuts:")
    print("  - Arrow keys: navigate text")
    print("  - Ctrl+A: beginning of line")
    print("  - Ctrl+E: end of line")
    print("  - Ctrl+K: delete to end")
    print("  - Ctrl+U: delete to beginning")
    print("  - Up/Down arrows: history")
    print("  - Type 'exit' or 'quit' to end, or Ctrl+C")
    print("-" * 40)
    
    readline.set_startup_hook(None)
    
    while True:
        try:
            sentence = input("Enter sentence to rephrase: ").strip()
            
            if sentence.lower() in ["exit", "quit"]:
                print("Exiting interactive mode.")
                break
            
            if not sentence:
                continue
            
            tone_input = input("Choose tone (neutral/polite/casual) [neutral]: ").strip().lower()
            tone = tone_input if tone_input in ["neutral", "polite", "casual"] else "neutral"
            
            try:
                rephrased = rephrase_sentence(sentence, tone, client, model, prompt)
                print(f"\nOriginal: {sentence}")
                print(f"Rephrased ({tone}): {rephrased}")
                
                subprocess.run("pbcopy", universal_newlines=True, input=rephrased)
                print("(Copied to clipboard)")
                print("-" * 40)
                
            except Exception as e:
                print(f"Error rephrasing: {e}")
                
        except KeyboardInterrupt:
            print("\nExiting interactive mode.")
            break
        except EOFError:
            print("\nExiting interactive mode.")
            break

def main():
    args = parse_arguments()
    
    # Check that the OpenAI API key is set.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: The OPENAI_API_KEY environment variable is not set.")
        exit(1)
    client = openai.OpenAI(api_key=api_key)

    if args.interactive:
        interactive_mode(client, args.model, args.prompt)
    else:
        if not args.sentence:
            print("Error: Sentence is required when not in interactive mode.")
            exit(1)
            
        tone = determine_tone(args)
        try:
            rephrased = rephrase_sentence(args.sentence, tone, client, args.model, args.prompt)
            print("\nRephrased sentence:")
            print(rephrased)
            # Copy the rephrased sentence to the clipboard on macOS using pbcopy.
            subprocess.run("pbcopy", universal_newlines=True, input=rephrased)
            print("\n(The rephrased sentence has been copied to your clipboard.)")
        except Exception as e:
            print(f"An error occurred while rephrasing the sentence: {e}")

if __name__ == "__main__":
    main()

