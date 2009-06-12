from tddspry.general.mock import Mock



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
        self.text = err
    def read(self):
        return self.text
