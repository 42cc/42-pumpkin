from pumpkin.pukorators import *
@given(r'I add (?P<num1>\d*) and (?P<num2>\d*)')
def add(num1,num2):
    global RESULTS
    RESULTS = int(num1) + int(num2)

@then(r'result should be (?P<res>\d*)')
def result(res):
    assert int(res) == RESULTS
