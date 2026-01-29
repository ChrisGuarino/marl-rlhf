# MARL-RLHF

A preference data collection framework for evaluating and comparing LLM-generated code, using Ollama to run local Llama 3.2 models against a suite of coding tasks.

## Overview

This project builds a pipeline for collecting preference data from LLM code generation. A judge system evaluates generated Python code against test suites, and a DPO-style comparison framework logs A/B preferences between model variants with different hyperparameters.

## How It Works

1. **Code generation** — A local Llama 3.2 model (via Ollama) receives a coding prompt and generates a Python function
2. **Judging** — The generated code is cleaned, extracted, and executed against predefined test cases
3. **Scoring** — Pass/fail rates are logged per task
4. **Preference collection** — Two model variants (different temperature, top_p, top_k, prompt style) generate competing solutions; the judge picks the winner

## Coding Tasks

The judge evaluates 9 coding tasks: `add`, `average`, `factorial`, `is_palindrome`, `reverse_words`, `is_prime`, `fizzbuzz`, `merge_sorted_lists`, `csv_to_dicts`.

## Scripts

| Script | Description |
|--------|-------------|
| `support.py` | Judge system — code cleanup, extraction, test execution, scoring |
| `loop_test.py` | Single-run evaluation loop, logs results to `logs/runs.jsonl` |
| `dpo_test.py` | A/B comparison of model variants, logs preferences to `logs/prefrences.jsonl` |
| `eval_candidate.py` | Standalone candidate code evaluator |
| `test_llama.py` | Basic Ollama connectivity test |
| `Modelfile` | Ollama model config (Llama 3.2:3b with system prompt) |

## Requirements

- Python 3
- [Ollama](https://ollama.com/) with Llama 3.2 model pulled locally

```bash
pip install -r requirements.txt
ollama pull llama3.2:3b
```

## Usage

```bash
# Create the custom Ollama model
ollama create ppo-llama -f Modelfile

# Run single evaluation loop
python loop_test.py

# Run A/B preference comparison
python dpo_test.py
```

Results are logged to `logs/`.

## Project Structure

```
marl-rlhf/
├── support.py            # Judge system and test suites
├── loop_test.py          # Single-run evaluation
├── dpo_test.py           # A/B preference collection
├── eval_candidate.py     # Candidate evaluator
├── test_llama.py         # Ollama connectivity test
├── Modelfile             # Custom Ollama model definition
├── data.jsonl            # Task prompts
├── data/                 # Additional data files
├── logs/                 # Evaluation and preference logs
├── requirements.txt
└── README.md
```
