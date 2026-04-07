# Python Local Chatbot

A simple, rule-based offline chatbot written entirely in standard Python without any external dependencies or APIs. 

## Features
- **Conversational**: Uses regex pattern-matching to respond to standard greetings and questions.
- **Math Solver**: Evaluates mathematical equations securely (e.g., `5 + 10` or `what is 100 / 2`).
- **Time & Date**: Checks the current local date and time.
- **Random Utilities**: Generate a coin flip or roll a 6-sided dice.
- **Jokes**: Tells random developer jokes.
- **Persistent Memory**: Can save notes into a secure local text file (`notes.txt`) and retrieve them later using conversational commands (e.g., `please note that my favorite language is Python`).

## How to Run
Since it relies only on Python standard libraries, no installation step is needed. Run the script directly:

```bash
python chatbot.py
```

Type `quit`, `bye`, or `exit` to end the conversation.
