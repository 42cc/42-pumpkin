from pumpkin.pukorators import *
@given('I think that 2+2=5')
def amiright():
    assert 2+2 == 5

@then('I think that 2+2=4')
def imright():
    assert 2+2 == 4    