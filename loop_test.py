# step2_eval_candidate.py
import ollama, statistics
from support import *  # your judge


LOG_PATH = "logs/runs.jsonl"
MODEL_ID = "ppo-llama"

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