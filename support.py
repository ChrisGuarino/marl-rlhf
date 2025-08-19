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
    code = clean_code(gen_code)
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
            passed = 0
            # passed = sum(
            #     1
            #     for nums, expected in zip(tests, answers)
            #     if ns["average"](nums) == expected
            # )
            # return passed / len(tests)
            for nums, expected in zip(tests, answers):
                if ns["average"](nums) == expected:
                    passed +=1 
                else: continue
            return passed/len(tests)
        # case "factorial":
        #     passed = sum(
        #         1
        #         for nums, expected in zip(tests, answers)
        #         if ns["average"](nums) == expected
        #     )
        #     return passed / len(tests)
        # case "is_palindrome":
        # case "reverse_words":
        # case "is_prime":
        # case "fizzbuzz":
        # case "merge_sorted_lists":
        # case "csv_to_dicts":
        case _:
            print(f'Unknown task command {task}.')
            
def score_is_palindrome_fix(tests, code_str: str) -> float:
    """Return fraction of tests passed for is_palindrome(s) ignoring case & spaces."""
    try:
        code = clean_code(code_str)
        ns = {}
        exec(code, ns, ns) 
        if "is_palindrome" not in ns or not callable(ns["is_palindrome"]):
            return 0.0

        passed = 0
        for s, expected in tests:
            got = ns["is_palindrome"](s)
            if isinstance(got, bool) and got == expected:
                passed += 1
                print(f'Test: {s}, Got: {got}, Expected: {expected}')
            else: print(f'⚠️Fail -> Test: {s}, Got: {got}, Expected: {expected}')
        return passed / len(tests)
    except Exception:
        traceback.print_exc()
        return 0.0

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
