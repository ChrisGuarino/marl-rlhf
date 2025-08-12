# expects: factorial(n)
def run_tests(ns):
    assert ns['factorial'](0) == 1
    assert ns['factorial'](1) == 1
    assert ns['factorial'](5) == 120
    return 3
