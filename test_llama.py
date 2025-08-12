import ollama

# Simple one-off generation (non-chat)
resp = ollama.generate(model='ppo-llama',
                       prompt='In RL, what does PPO stand for? Answer in one sentence.')
print(resp['response'])