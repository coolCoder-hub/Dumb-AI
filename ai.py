import os
import re

# Load knowledge files into a dictionary
def load_knowledge(base_path):
    knowledge = {}
    for filename in os.listdir(base_path):
        if filename.endswith(".txt"):
            topic = filename.replace(".txt", "")
            with open(os.path.join(base_path, filename), "r") as file:
                knowledge[topic] = [line.strip() for line in file.readlines()]
    return knowledge

# Clean and standardize text for matching
def clean_text(text):
    return re.sub(r"[^\w\s\+\=\*]", "", text).strip().lower()

# Extract math operation from a question like 'what is 2+2'
def extract_math_problem(question):
    # Remove any unnecessary words before math operation
    math_question = re.sub(r"[^0-9\+\-\*\=/]", "", question)
    return math_question

# Solve math problems like addition and multiplication
def solve_math_problem(question):
    # Clean and extract math problem from the input question
    cleaned_question = extract_math_problem(question)

    try:
        # Handling addition or multiplication questions
        if '+' in cleaned_question:
            num1, num2 = map(int, cleaned_question.split('+'))
            return f"{num1} + {num2} = {num1 + num2}"
        elif '*' in cleaned_question:
            num1, num2 = map(int, cleaned_question.split('*'))
            return f"{num1} * {num2} = {num1 * num2}"
        else:
            return "I can only solve addition and multiplication problems."
    except Exception as e:
        return f"Error: {e}"

# Find the best matching answer from the knowledge base
def find_answer(question, knowledge):
    cleaned_question = clean_text(question)
    best_match = None
    best_score = 0

    for topic, lines in knowledge.items():
        for line in lines:
            cleaned_line = clean_text(line)

            # 1. Exact match (Highest Priority)
            if cleaned_question == cleaned_line:
                return line

            # 2. Word-order match (Medium Priority)
            if all(word in cleaned_line for word in cleaned_question.split()):
                score = sum(word in cleaned_line for word in cleaned_question.split())
                if score > best_score:
                    best_match = line
                    best_score = score

            # 3. Partial match (Lowest Priority)
            elif any(word in cleaned_line for word in cleaned_question.split()):
                score = sum(word in cleaned_line for word in cleaned_question.split())
                if score > best_score:
                    best_match = line
                    best_score = score

    return best_match if best_match else "I don't know the answer to that."

# Main loop
knowledge_base = load_knowledge("knowledge")
print("Dumb AI: Ask me a question! (Type 'exit' to quit)")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    # First, check if it's a math question (addition or multiplication)
    if '+' in user_input or '*' in user_input:
        response = solve_math_problem(user_input)
    else:
        # If not, search the knowledge base
        response = find_answer(user_input, knowledge_base)
    
    print("Dumb AI:", response)
