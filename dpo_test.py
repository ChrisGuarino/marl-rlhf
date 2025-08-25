# step2_eval_candidate.py
import ollama, statistics
from support import *

DATA_PATH = "data.jsonl"
LOG_PATH = "logs/prefrences.jsonl"
MODEL_ID = "ppo-llama"

def verus_run(temp=0.9):
    for entry in iter_jsonl("data.jsonl"):
        task   = entry["task"]          # e.g., "add"
        prompt = entry["prompt"]        # the exact prompt
        tests  = entry["tests"]         # list of tests for the task
        answers = entry["answers"]
        # -> call model, run judge for `task`, compute reward, log
        #1) Call local LLMs with different temps
        temp_a = 0.9
        temp_b = 0.2
        agent_a = ollama.generate(model=MODEL_ID, prompt=prompt, options={"temperature": temp_a})
        agent_b = ollama.generate(model=MODEL_ID, prompt=prompt, options={"temperature": temp_b})
        code_a = agent_a["response"]
        code_b = agent_b["response"]

        print(f"\n🟢--- CANDIDATE {task} ---")
        #2) Score the generated code
        print('Agent A')
        reward_a,failed_a,errors_a = score_code(task, code_a, tests, answers)
        print('Agent B')
        reward_b,failed_b,errors_b = score_code(task, code_b, tests, answers)
        print(f"🔴--- SCORE: agent_a:{reward_a} vs. agent_b:{reward_b} ---") 

        #Compare the different agents
        winner = ""
        if reward_a > reward_b:
            winner = "A"
        elif reward_b > reward_a:
            winner = "B"
        else: winner = "TIE"

        #3) Log the reward
        rec = {
            "ts": now_iso(),
            "task_id": task,
            "reward": (reward_a,reward_b),
            "failed": (failed_a,failed_b),
            "errors": (errors_a,errors_b),
            "prompt": prompt,
            "model": MODEL_ID,
            "options": {"temperature": (temp_a,temp_b)},
            "response": (code_a,code_b),
            "winner": winner
        }
        append_jsonl(LOG_PATH, rec)
        
        # 4) quick console feedback
        print("Logged to:", LOG_PATH)

        #Compare scores 
    return 

for _ in range(1): 
    verus_run()
