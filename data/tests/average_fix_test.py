# expects: average(nums)
def run_tests(ns):
    assert abs(ns['average']([1,2,3,4]) - 2.5) < 1e-9
    assert abs(ns['average']([10]) - 10.0) < 1e-9
    try:
        ns['average']([])
    except Exception:
        pass
    else:
        raise AssertionError("average should raise on empty list")
    return 3
