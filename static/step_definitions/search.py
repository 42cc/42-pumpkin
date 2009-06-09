from pukorators import given,when,then
from twill.commands import go, code, show, find, notfind, formvalue, submit

@given("I am on the Google search page")
def go_google():
    go('http://www.google.com/')

@when(r'I search for "(?P<query>.*)"')
def search_for_query(query):
  formvalue(1, 'q', query)
  submit()
  code('200')

@then(r'I should see a link to "(?P<expected_url>.*)"')
def should_have_link(expected_url):
  find('<a.*href="http://%s/"' % expected_url)

