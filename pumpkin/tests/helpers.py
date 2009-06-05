from tddspry.general.mock import Mock

def importCode(code, name):
    """ code can be any object containing code -- string,
    file object, or compiled code object. Returns a new module object initialized by dynamically importing the given code and optionally adds it  to sys.modules under the given name.
    """
    import imp
    module = imp.new_module(name)
    exec code in module.__dict__
    return module


class Mockstd(Mock):
    """
    mocking sys.stderr
    warning: method sys.stderr.read() used in tests
    working correctly only with mocked stderr.

    real stderr does not return EOF
    """
    def __init__(self):
        self.text = ""
    def write(self, err):
        self.text += err
    def read(self):
        return self.text
