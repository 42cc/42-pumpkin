from pumpkin.pukorators import *
@given(r'I think : (?P<var1>\d) [+] (?P<var2>\d) = (?P<var3>\d)')
def amiright_again(var1,var2,var3):
    assert int(var1) + int(var2) == int(var3)

@when(r'answer is (?P<digit>\d), then it sounds "(?P<word>.*)"')
def digit_is_word(digit,word):
    if digit == "1":
        assert word == "one"
    elif digit == "5":
        assert word == "five"
    else:
        raise Exception
