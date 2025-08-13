# step2_eval_candidate.py
import ollama
from tests import score_add_fix  # your judge

PROMPT = """The following function is supposed to add two numbers, but it has a bug.
Return ONLY the corrected Python function. Do NOT include backticks or explanation.
Start your answer with: def add(

def add(a, b):
    return a - b
"""

resp = ollama.generate(
    model="ppo-llama",   # or "llama3.2:3b" if you didn’t make the custom model
    prompt=PROMPT,
    options={"temperature": 0}  # deterministic for easier debugging
)

code = resp["response"]
reward = score_add_fix(code)
print("MODEL OUTPUT:\n", code)
print("\nREWARD:", reward)
