#!/usr/bin/env python3
import argparse
import os
import openai
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Rephrase a sentence using OpenAI's gpt-3.5-turbo with a specified tone."
    )
    parser.add_argument("sentence", help="The sentence you want to rephrase.")
    
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

def rephrase_sentence(sentence: str, tone: str, client: openai.Client) -> str:
    # Build the conversation messages for ChatCompletion
    system_message = "You are a helpful assistant that rephrases text."
    user_prompt = f"Rephrase the following sentence in a {tone} tone without including any quotes:\n\n\"{sentence}\""

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.7)

    # Extract and return the rephrased sentence.
    return response.choices[0].message.content.strip()

def main():
    args = parse_arguments()
    tone = determine_tone(args)

    # Check that the OpenAI API key is set.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: The OPENAI_API_KEY environment variable is not set.")
        exit(1)
    client = openai.OpenAI(api_key=api_key)

    try:
        rephrased = rephrase_sentence(args.sentence, tone, client)
        print("\nRephrased sentence:")
        print(rephrased)
        # Copy the rephrased sentence to the clipboard on macOS using pbcopy.
        subprocess.run("pbcopy", universal_newlines=True, input=rephrased)
        print("\n(The rephrased sentence has been copied to your clipboard.)")
    except Exception as e:
        print(f"An error occurred while rephrasing the sentence: {e}")

if __name__ == "__main__":
    main()

