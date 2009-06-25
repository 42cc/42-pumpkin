# -*- coding: utf-8 -*-
from pukorators import given,when,then
from twill.commands import go, code, url, show, showforms, find, notfind, formvalue, submit

@given(r'я на сторінці пошуку Google')
def go_google():
    go('http://www.google.com/')

@when(r'я ввожу „(?P<query>.*)“')
def input(query):
    formvalue(1, 'q', query)

@when(r'натискаю „Мені пощастить“')
def press():
    submit(5)
    code('200')

@then(r'маю перейти на (?P<expected_url>.*)')
def check_page(expected_url):
    url('http://'+expected_url+'/')

@when(r'я шукаю "(?P<query>.*)"')
def search_for_query(query):
    formvalue(1, 'q', query)
    submit()
    code('200')


@then(r'кількість результатів буде (\d*)')
#actually fails, because number of results changes to often :)
def result_num(n1):
    #show()
    find(n1[:1]+'&nbsp;'+ n1[1:4]+'&nbsp;'+n1[4:])
