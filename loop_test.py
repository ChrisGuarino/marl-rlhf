# step2_eval_candidate.py
import ollama, statistics
from support import *  # your judge


LOG_PATH = "logs/runs.jsonl"
MODEL_ID = "ppo-llama"

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

Requirements:
- Return True if s is a palindrome ignoring CASE and SPACES.

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
    ("ab!ba", True),  
    ("snakes", False)
]
#####################

def one_run(temp=0.9):
    #1) Call local LLM
    resp = ollama.generate(model=MODEL_ID, prompt=PROMPT, options={"temperature": temp})
    code = resp["response"]

    #2) Score the generated code
    reward = score_is_palindrome_fix(tests, code)
    print("\n--- CANDIDATE ---\n", code, "\nSCORE:", reward) 

    #3) Log the reward
    rec = {
        "ts": now_iso(),
        "task_id": "testing",
        "model": MODEL_ID,
        "options": {"temperature": temp},
        "prompt": PROMPT,
        "response": code,
        "reward": reward,
    }
    append_jsonl(LOG_PATH, rec)
    
    # 4) quick console feedback
    print("Reward:", reward)
    print("Logged to:", LOG_PATH)

    return reward
scores = [one_run() for _ in range(5)]
print("\nSUMMARY -> scores:", scores, "avg:", statistics.mean(scores))