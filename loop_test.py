# step2_eval_candidate.py
import ollama, statistics
from support import *

DATA_PATH = "data.jsonl"
LOG_PATH = "logs/runs.jsonl"
MODEL_ID = "ppo-llama"

def one_run(temp=0.9):
    for entry in iter_jsonl("data.jsonl"):
        task   = entry["task"]          # e.g., "add"
        prompt = entry["prompt"]        # the exact prompt
        tests  = entry["tests"]         # list of tests for the task
        answers = entry["answers"]
        # -> call model, run judge for `task`, compute reward, log
        #1) Call local LLM
        resp = ollama.generate(model=MODEL_ID, prompt=prompt, options={"temperature": temp})
        code = resp["response"]
        print(f"\n--- CANDIDATE {task} ---\n")
        print(code)
        #2) Score the generated code
        reward = score_code(task, code, tests, answers)
        print(f"--- SCORE: {reward} ---\n") 

        #3) Log the reward
        rec = {
            "ts": now_iso(),
            "task_id": task,
            "model": MODEL_ID,
            "options": {"temperature": temp},
            "prompt": prompt,
            "response": code,
            "reward": reward,
        }
        append_jsonl(LOG_PATH, rec)
        
        # 4) quick console feedback
        print("Logged to:", LOG_PATH)

    return reward
scores = one_run()
print("\nSUMMARY -> scores:", scores, "avg:", statistics.mean(scores))