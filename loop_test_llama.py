# step2_eval_candidate.py
import ollama, statistics
from tests import *  # your judge

##### Test Prompts #####

# Adding
# PROMPT = """The following function is supposed to add two numbers, but it has a bug.
# Return ONLY the corrected Python function. Do NOT include backticks or explanation.
# Start your answer with: def add(

# def add(a, b):
#     return a - b
# """

# Palindrome
PROMPT = """You are fixing a buggy Python function.
Return ONLY the corrected Python function. Do NOT include backticks or explanations.
Start your answer with: def is_palindrome(

# The function should return True if s is a palindrome ignoring case and spaces.
# Buggy version:
def is_palindrome(s):
    return s == s[::-1]
"""
########################

##### Test Data #####

tests = [
    ("racecar", True),
    ("Race Car", True),
    ("nurses run", True),
    ("hello", False),
    ("A man a plan a canal Panama", True),
    ("", True),
    ("   ", True),
    ("abc cba", True),
    ("ab!ba", False),   # NEW: punctuation should NOT be ignored
]

#####################

def one_try(temp=0.7):
    resp = ollama.generate(model="ppo-llama", prompt=PROMPT, options={"temperature": temp})
    code = resp["response"]
    score = score_is_palindrome_fix(tests, code)
    print("\n--- CANDIDATE ---\n", code, "\nSCORE:", score)  # helpful to see what it produced
    return score

scores = [one_try() for _ in range(5)]
print("\nSUMMARY -> scores:", scores, "avg:", statistics.mean(scores))