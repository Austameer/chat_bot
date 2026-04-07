import re
import random
import datetime
import os

class SimpleChatbot:
    def __init__(self):
        # Define patterns and corresponding responses
        # The patterns are regular expressions
        self.rules = [
            (r'hi|hello|hey|greetings', ['Hello!', 'Hi there!', 'Hey! How can I help you today?']),
            (r'how are you(.*)', ['I am just a computer program, but I am doing well! How are you?', 'Doing great, thanks for asking!']),
            (r'what is your name(.*)', ['I am a simple rule-based chatbot written in Python.', 'You can call me PyBot!']),
            (r'(.*) time is it(.*)', ['I don\'t have a watch, but you can check your system clock!']),
            (r'my name is (.*)', ['Nice to meet you, {0}!', 'Hello {0}, how can I assist you?']),
            (r'(.*) help (.*)', ['I can try to help! What do you need assistance with?']),
            (r'(.*) your favorite (.*)', ['I don\'t really have favorites since I\'m just code, but I love chatting!']),
            (r'bye|goodbye|quit|exit', ['Goodbye! Have a great day!', 'Bye! See you later.', 'It was nice talking to you!']),
            # A catch-all default response if nothing matches
            (r'(.*)', ["I'm sorry, I don't quite understand.", "Could you try rephrasing that?", "Interesting, tell me more!"])
        ]

    def evaluate_math(self, expression):
        try:
            # Clean the expression to only allow digits and basic math operators for safety
            clean_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            if not clean_expr.strip():
                return None
            
            # Evaluate using restricted environment to avoid code injection
            result = eval(clean_expr, {"__builtins__": None}, {})
            
            # Remove trailing .0 for whole numbers to make it look nicer
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            return str(result)
        except Exception:
            # If the math is invalid (e.g. division by zero), return None
            return None

    def get_response(self, user_input):
        # Convert user input to lowercase to make matching easier
        user_input_lower = user_input.lower()
        
        # --- Feature 1: Time and Date ---
        if "time" in user_input_lower and ("what" in user_input_lower or "current" in user_input_lower):
            return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
            
        if "date" in user_input_lower and ("what" in user_input_lower or "current" in user_input_lower or "today" in user_input_lower):
            return f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}."
            
        # --- Feature 2: Random Utilities (Coin and Dice) ---
        if "flip a coin" in user_input_lower or "coin flip" in user_input_lower:
            return f"I flipped a coin and got: {random.choice(['Heads', 'Tails'])}!"
            
        if "roll a dice" in user_input_lower or "roll dice" in user_input_lower:
            return f"I rolled a 6-sided dice and got: {random.randint(1, 6)}!"
            
        # --- Feature 3: Entertainment (Jokes) ---
        if "joke" in user_input_lower and ("tell" in user_input_lower or "hear" in user_input_lower):
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why did the developer go broke? Because he used up all his cache!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
                "What's the object-oriented way to become wealthy? Inheritance!"
            ]
            return random.choice(jokes)
            
        # --- Feature 4: Persistent Memory (Saving and Reading Notes) ---
        if "what are my notes" in user_input_lower or "read notes" in user_input_lower or "read my notes" in user_input_lower:
            if os.path.exists("notes.txt"):
                with open("notes.txt", "r") as f:
                    notes = f.readlines()
                if notes:
                    notes_str = "\n".join([f"- {n.strip()}" for n in notes])
                    return f"Here are your saved notes:\n{notes_str}"
            return "You don't have any saved notes yet."
            
        note_match = re.search(r'^(?:please )?(?:take a )?(?:note|remember)(?: that)? (.+)', user_input_lower)
        if note_match:
            note_content = note_match.group(1).strip()
            with open("notes.txt", "a") as f:
                f.write(note_content + "\n")
            return f"Got it! I have saved the note: '{note_content}'"
        
        # --- Feature 5: Mathematical Expressions ---
        # Matches numbers optionally followed by decimals, an operator, and more numbers/operators
        math_match = re.search(r'([0-9]+(?:\.[0-9]+)?\s*[\+\-\*\/]\s*[0-9\+\-\*\/\.\s()]+)', user_input_lower)
        if math_match:
            expr = math_match.group(1)
            result = self.evaluate_math(expr)
            if result is not None:
                return f"That's easy! The answer is {result}."

        # --- Feature 6: Check against standard conversation rules ---
        for pattern, responses in self.rules:
            match = re.search(pattern, user_input_lower)
            if match:
                # Choose a random response from the available options
                response = random.choice(responses)
                
                # If the pattern has capture groups (like 'my name is (.*)'), 
                # we can format the response with the captured text
                groups = match.groups()
                if groups and '{0}' in response:
                    # Replace {0} with the first captured group
                    response = response.format(groups[0].strip())
                    
                return response
                
        return "I'm not sure how to respond."

def start_chat():
    bot = SimpleChatbot()
    print("🤖 ChatBot started! Type 'quit' or 'bye' to exit.")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("You: ")
            
            # Check for exit commands explicitly as well
            if user_input.lower() in ['quit', 'bye', 'exit', 'goodbye']:
                print("🤖 ChatBot: Goodbye!")
                break
                
            response = bot.get_response(user_input)
            print(f"🤖 ChatBot: {response}")
            
        except (KeyboardInterrupt, EOFError):
            print("\n🤖 ChatBot: Goodbye!")
            break

if __name__ == "__main__":
    start_chat()
