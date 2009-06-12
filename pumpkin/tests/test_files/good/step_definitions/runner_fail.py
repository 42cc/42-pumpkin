from pumpkin.pukorators import *
@given(r'I think that \d [+] \d = \d')
def amiright():
    assert 2 + 2 == 5
