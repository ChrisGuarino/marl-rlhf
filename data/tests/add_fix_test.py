# expects: add(a, b)
def run_tests(ns):
    assert ns['add'](1, 2) == 3
    assert ns['add'](-1, 5) == 4
    assert ns['add'](0, 0) == 0
    return 3
