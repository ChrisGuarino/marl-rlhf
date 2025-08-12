# expects: is_palindrome(s)
def run_tests(ns):
    assert ns['is_palindrome']("racecar") is True
    assert ns['is_palindrome']("Race Car") is True
    assert ns['is_palindrome']("hello") is False
    return 3
