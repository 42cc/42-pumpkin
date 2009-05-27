def importCode(code, name):
    """ code can be any object containing code -- string,
    file object, or compiled code object. Returns a new module object initialized by dynamically importing the given code and optionally adds it  to sys.modules under the given name.
    """
    import imp
    module = imp.new_module(name)
    exec code in module.__dict__
    return module
