from pydebug import env_helpers


def test_inspect_ops(mocker):
    mocker.patch.dict('os.environ', {'DEBUG_COLORS': 'no',
                                     'DEBUG_DEPTH': '10',
                                     'DEBUG_SHOW_HIDDEN': 'enabled',
                                     'DEBUG_SOMETHING': 'null'})
    # mocker.patch('os.environ.keys', return_value=['DEBUG_COLORS'])
    # mocker.patch('os.environ.get', )
    actual = env_helpers.inspect_ops()
    assert actual == {'colors': False, 'depth': 10, 'show_hidden': True, 'something': None}


def test_load_and_save():
    actual = env_helpers.load()
    assert actual == ''

    env_helpers.save('test:data')
    actual = env_helpers.load()
    assert actual == 'test:data'
