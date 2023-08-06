from toys.toys.toy1 import foo


def import_foo():
    ret = foo()
    return f'\ntoy2 get {ret}\n'
