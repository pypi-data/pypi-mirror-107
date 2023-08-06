from toys.toy2 import import_foo


def test_import_foo(mocker):
    mocker.patch('toys.toy2.foo', return_value='mocked value')
    ret = import_foo()
    print(ret)
