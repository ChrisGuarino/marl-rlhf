# expects: fib(n)
def run_tests(ns):
    assert ns['fib'](0) == 0
    assert ns['fib'](1) == 1
    assert ns['fib'](7) == 13
    return 3
