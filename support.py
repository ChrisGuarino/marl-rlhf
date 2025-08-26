# A tiny judge: takes model output (a code string), returns a reward in [0,1].
import re
from typing import Tuple, Dict
import math

def clean_code(code_str: str) -> Tuple[str, Dict[str, int]]:
    tally = {
        "trim_calls": 0,
        "fences_removed": 0,
        "prefix_fence_removed": 0,
        "suffix_fence_removed": 0,
        "backticks_stripped": 0,
        "def_anchor_used": 0,
    }

    s = code_str
    before = s
    s = s.strip()
    if s != before:
        tally["trim_calls"] += 1

    # ```python / ```py prefix
    new_s, n = re.subn(r"^\s*```(?:python|py)?\s*", "", s, flags=re.I | re.M)
    if n:
        tally["prefix_fence_removed"] += n
        tally["fences_removed"] += n
    s = new_s

    # ``` suffix
    new_s, n = re.subn(r"\s*```\s*$", "", s, flags=re.I | re.M)
    if n:
        tally["suffix_fence_removed"] += n
        tally["fences_removed"] += n
    s = new_s

    # any leftover ``` in the middle
    bt_count = s.count("```")
    if bt_count:
        tally["backticks_stripped"] += bt_count
        s = s.replace("```", "")

    # keep from first def ...(
    m = re.search(r"(^\s*def\s+[A-Za-z_]\w*\s*\(.*)", s, flags=re.S | re.M)
    if m:
        tally["def_anchor_used"] += 1
        s = s[m.start():]

    s = s.strip()
    return s, tally


LOG_PATH = "logs/errors.jsonl"

def score_code(task, gen_code, tests, answers):
    errors = []
    failed = []
    try:
        code, tally = clean_code(gen_code)
        print(code)
        ns = {}
        exec(code, ns, ns)
        match task: 
            case "add":
                passed = 0
                for (a,b),expected in zip(tests, answers): 
                    try: 
                        if ns["add"](a,b) == expected:
                            passed +=1
                        else: 
                            print(f'FAILED: test = {a,b}, answer = {expected}, result = {ns["add"](a,b)}')
                            failed.append([(a,b),expected,ns["add"](a,b)])
                    except Exception as e: 
                        print(f'⚠️ ERROR: {e}')
                        errors.append(str(e))
            case "average":
                passed = 0
                for nums,expected in zip(tests, answers): 
                    try: 
                        if math.isclose(ns["average"](nums),expected):
                            passed +=1
                        else: 
                            print(f'FAILED: test = {nums}, answer = {expected}, result = {ns["average"](nums)}')
                            failed.append([nums,expected,ns["average"](nums)])
                    except Exception as e: 
                        print(f'⚠️ ERROR: {e}')
                        errors.append(str(e))
            case "factorial":
                passed = 0
                for n,expected in zip(tests, answers): 
                    try: 
                        if ns["factorial"](n) == expected:
                            passed +=1
                        else: 
                            print(f'FAILED: test = {n}, answer = {expected}, result = {ns["factorial"](n)}')
                            failed.append([n,expected,ns["factorial"](n)])
                    except Exception as e: 
                        print(f'⚠️ ERROR: {e}')
                        errors.append(str(e))
            case "is_palindrome":
                passed = 0
                for s,expected in zip(tests, answers): 
                    try: 
                        if ns["is_palindrome"](s) == expected:
                            passed +=1
                        else: 
                            print(f'FAILED: test = {s}, answer = {expected}, result = {ns["is_palindrome"](s)}')
                            failed.append([s,expected,ns["is_palindrome"](s)])
                    except Exception as e: 
                        print(f'⚠️ ERROR: {e}')
                        errors.append(str(e))
            case "reverse_words":
                passed = 0
                for s,expected in zip(tests, answers): 
                    try: 
                        if ns["reverse_words"](s) == expected:
                            passed +=1
                        else: 
                            print(f'FAILED: test = {s}, answer = {expected}, result = {ns["reverse_words"](s)}')
                            failed.append([s,expected,ns["reverse_words"](s)])
                    except Exception as e: 
                        print(f'⚠️ ERROR: {e}')
                        errors.append(str(e))
            case "is_prime":
                passed = 0
                for n,expected in zip(tests, answers): 
                    try: 
                        if ns["is_prime"](n) == expected:
                            passed +=1
                        else: print(f'FAILED: test = {n}, answer = {expected}, result = {ns["is_prime"](n)}')
                        failed.append([n,expected,ns["is_prime"](n)])
                    except Exception as e: 
                        print(f'⚠️ ERROR: {e}')
                        errors.append(str(e))
            case "fizzbuzz":
                passed = 0
                for n,expected in zip(tests, answers): 
                    try: 
                        if ns["fizzbuzz"](n) == expected:
                            passed +=1
                        else: 
                            print(f'FAILED: test = {n}, answer = {expected}, result = {ns["fizzbuzz"](n)}')
                            failed.append([n,expected,ns["fizzbuzz"](n)])
                    except Exception as e: 
                        print(f'⚠️ ERROR: {e}')
                        errors.append(str(e))
            case "merge_sorted_lists":
                passed = 0
                for (a,b),expected in zip(tests, answers): 
                    try: 
                        if ns["merge_sorted_lists"](a,b) == expected:
                            passed +=1
                        else: 
                            print(f'FAILED: test = {a,b}, answer = {expected}, result = {ns["merge_sorted_lists"](a,b)}')
                            failed.append([(a,b),expected,ns["merge_sorted_lists"](a,b)])
                    except Exception as e: 
                        print(f'⚠️ ERROR: {e}')
                        errors.append(str(e))
            case "csv_to_dicts":
                passed = 0
                for s,expected in zip(tests, answers): 
                    try: 
                        if ns["csv_to_dicts"](s) == expected:
                            passed +=1
                        else: 
                            print(f'FAILED: test = {s}, answer = {expected}, result = {ns["csv_to_dicts"](s)}')
                            failed.append([s,expected,ns["csv_to_dicts"](s)])
                    except Exception as e: 
                        print(f'⚠️ ERROR: {e}')
                        errors.append(str(e))
        pass_score = passed/len(tests)
        return pass_score,failed,errors,tally
    except: 
        print(f'Task {task} not recognized.')
        return 0.0,failed,errors,tally

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
