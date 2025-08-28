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
        #1) Call local LLMs with different hyperparameters
        #TEMP
        temp_a = 0.9
        temp_b = 0.0
        #Top_p
        top_p_a = 0.95
        top_p_b = 1.0
        #Top_k
        top_k_a = 100
        top_k_b = 0

        #Adjust prompt style
        style_a = " Return the smallest correct solution. No input checks."
        style_b = " Include basic input validation and handle edge cases."

        agent_a = ollama.generate(model=MODEL_ID, prompt=prompt+style_a, options={"temperature": temp_a, "top_p": top_p_a, "top_k": top_k_a, "mirostat": 2})
        agent_b = ollama.generate(model=MODEL_ID, prompt=prompt+style_b, options={"temperature": temp_b, "top_p": top_p_b, "top_k": top_k_b})
        code_a = agent_a["response"]
        code_b = agent_b["response"]

        print(f"\n🟢--- CANDIDATE {task} ---")
        #2) Score the generated code
        print('➡ Agent A')
        reward_a,failed_a,errors_a,tally_a = score_code(task, code_a, tests, answers)
        print('➡ Agent B')
        reward_b,failed_b,errors_b,tally_b = score_code(task, code_b, tests, answers)
        print(f"🔴--- SCORE: agent_a:{reward_a} vs. agent_b:{reward_b} ---")

        #Compare the different agents
        winner = ""
        if reward_a > reward_b:
            winner = "A"
        elif reward_b > reward_a:
            winner = "B"
        else: 
            winner = "TIE"
            #Execute Tie Breaker
            

        #3) Log the reward
        rec = {
            "ts": now_iso(),
            "task_id": task,
            "prompt": prompt,
            "style_a": style_a,
            "style_b": style_b,
            "reward_a": reward_a,
            "reward_b": reward_b,
            "winner": winner,
            "failed_a": failed_a,
            "failed_b": failed_b,
            "errors_a": errors_a,
            "errors_b": errors_b,
            "clean_tally_a": tally_a,
            "clean_tally_b": tally_b,
            "options_a": {"temperature": temp_a,"top_p": top_p_a, "top_k": top_k_a},
            "options_b": {"temperature": temp_b,"top_p": top_p_b, "top_k": top_k_b},
            "raw_response_a": code_a,
            "raw_response_b": code_b,
            "clean_response_a": clean_code(code_a),
            "clean_response_b": clean_code(code_b)
        }
        append_jsonl(LOG_PATH, rec)
        
        # 4) quick console feedback
        print("Logged to:", LOG_PATH)

        #Compare scores 
    return 

for _ in range(1): 
    print('〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️')
    verus_run()
