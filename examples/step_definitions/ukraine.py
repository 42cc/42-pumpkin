# -*- coding: utf-8 -*-
from pukorators import *
@given(r'Я говорю українскьою')
def ukr():
    pass


@then(r'І в решті решт я гадаю що (\d) [+] (\d) = (\d)')
def add(num1,num2,result):
    assert num1+num2 == result
