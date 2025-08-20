# A tiny judge: takes model output (a code string), returns a reward in [0,1].

import re, traceback

def clean_code(code_str: str) -> str:
    s = code_str.strip()
    # strip ``` fences if present
    s = re.sub(r"^\s*```(?:python|py)?\s*", "", s, flags=re.I | re.M)
    s = re.sub(r"\s*```\s*$", "", s, flags=re.I | re.M)
    s = s.replace("```", "")
    # keep from first function definition onward
    m = re.search(r"(^\s*def\s+[A-Za-z_]\w*\s*\(.*)", s, flags=re.S | re.M)
    if m:
        s = s[m.start():]
    return s.strip()


def score_code(task, gen_code, tests, answers):
    try:
        code = clean_code(gen_code)
        print(code)
        ns = {}
        exec(code, ns, ns)
        match task: 
            case "add":
                passed = sum(
                    1 
                    for (a,b), expected in zip(tests, answers) #zip interates two lists at once
                    if ns["add"](a,b) == expected
                )
                return passed / len(tests)
            case "average":
                passed = sum(
                    1
                    for nums, expected in zip(tests, answers)
                    if ns["average"](nums) == expected
                )
                return passed / len(tests)
            case "factorial":
                passed = sum(
                    1
                    for n, expected in zip(tests, answers)
                    if ns["factorial"](n) == expected
                )
                return passed / len(tests)
            case "is_palindrome":
                passed = sum(
                    1
                    for s, expected in zip(tests, answers)
                    if ns["is_palindrome"](s) == expected
                )
                return passed / len(tests)
            case "reverse_words":
                passed = sum(
                    1
                    for s, expected in zip(tests, answers)
                    if ns["reverse_words"](s) == expected
                )
                return passed / len(tests)
            case "is_prime":
                passed = sum(
                    1
                    for n, expected in zip(tests, answers)
                    if ns["is_prime"](n) == expected
                )
                return passed / len(tests)
            case "fizzbuzz":
                passed = sum(
                    1
                    for n, expected in zip(tests, answers)
                    if ns["fizzbuzz"](n) == expected
                )
                return passed / len(tests)
            case "merge_sorted_lists":
                passed = sum(
                    1
                    for a,b, expected in zip(tests, answers)
                    if ns["merge_sorted_lists"](a,b) == expected
                )
                return passed / len(tests)
            case "csv_to_dicts":
                passed = sum(
                    1
                    for csv_str, expected in zip(tests, answers)
                    if ns["csv_to_dicts"](csv_str) == expected
                )
                return passed / len(tests)
            case _:
                print(f'Unknown task command {task}.')
    except: print("⚠️CASE Fault")  

import json, os, time
from typing import Any, Dict, Iterator

def append_jsonl(path: str, record: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

def iter_jsonl(path: str) -> Iterator[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            try:
                yield json.loads(s)
            except json.JSONDecodeError:
                # skip malformed lines
                continue
