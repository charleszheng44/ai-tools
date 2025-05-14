# AI Tools

This repository offers a suite of command-line AI utilities designed to assist with a variety of everyday tasks. 90% of scripts are written by AI.

## Available Tools

### 1. Rephrase (`rephrase`)

A command-line tool to rephrase a sentence using an OpenAI model. You can specify the desired tone (neutral, polite, casual) and the model to use.

**Usage:**

```bash
rephrase "your sentence here" [options]
```

**Options:**

*   `--model <model_name>`: Specify the OpenAI model (default: gpt-4o).
*   `--prompt "<custom_prompt>"`: Add a custom prefix to the rephrasing prompt.
*   `--neutral`: Rephrase in a neutral tone (default).
*   `--polite`: Rephrase in a polite tone.
*   `--casual`: Rephrase in a casual tone.

**Example:**

```bash
rephrase "I need this done now." --polite
```

The rephrased sentence will be printed to the console and copied to your clipboard (on macOS).

### 2. Terminal Chat (`chat`)

A command-line tool to engage in a continuous conversation with an OpenAI model directly in your terminal.

**Usage:**

```bash
chat [options]
```

**Options:**

*   `--model <model_name>`: Specify the OpenAI model to chat with (default: gpt-4o).
*   `--system-prompt "<prompt_text>"`: Set an initial system prompt to guide the AI's behavior (default: "You are a helpful assistant.").

**Example:**

```bash
chat --system-prompt "You are a Shakespearean poet."
```

Once started, type your messages and press Enter. The AI's responses will be displayed. Type `exit` or `quit` to end the chat session.

## Setup

1.  Ensure Python 3 is installed.
2.  Install the OpenAI Python library: `pip install openai`
3.  Set your OpenAI API key as an environment variable: `export OPENAI_API_KEY='your_api_key_here'`
4.  Make sure the scripts in the `bin` directory are executable and in your PATH. For example, `chmod +x bin/*` and add the `bin` directory to your PATH.
