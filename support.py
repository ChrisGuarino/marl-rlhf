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

def score_add_fix(code_str: str) -> float:
    """Return fraction of tests passed for the add(a,b) function."""
    try:
        code = clean_code(code_str)
        ns = {}
        exec(code, ns, ns)# executes 'code' and writes into ns globally and locally
        if "add" not in ns or not callable(ns["add"]):
            return 0.0

        tests = [(1,2,3), (-1,5,4), (0,0,0)]
        passed = sum(1 for a,b,exp in tests if ns["add"](a,b) == exp)
        return passed / len(tests)
    except Exception:
        traceback.print_exc()  # helpful while developing
        return 0.0
    
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
from typing import Any, Dict

def append_jsonl(path: str, record: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

