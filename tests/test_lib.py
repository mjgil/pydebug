
from pydebug import lib


def test_humanize():
    # from pydebug import lib
    ms = 1000
    sec = 1000 * ms
    min = 60 * sec
    hour = 60 * min
    assert lib.humanize(3) == '3us'
    assert lib.humanize(ms) == '1.0ms'
    assert lib.humanize(sec + 500 * ms) == '1.5s'
    assert lib.humanize(min) == '1.0m'
    assert lib.humanize(hour + 15 * min) == '1.2h'


def test_to_utc_string():
    # from pydebug import lib
    assert lib.to_utc_string(1366560000) == 'Sun, 21 Apr 2013 16:00:00 GMT'


def test_enable():
    # from pydebug import lib
    assert not lib.enabled('test')
    lib.enable('test:a:b,test:c:*,-examples:*')

    assert lib.enabled('test:a:b')
    assert not lib.enabled('test:a')
    assert lib.enabled('test:c:something')
    assert not lib.enabled('test:c')
    assert not lib.enabled('test:d')
    assert not lib.enabled('examples:a')
    assert lib.enabled('tada*')


def test_color():
    assert lib.color() == 6
    assert lib.color() == 2
    assert lib.color() == 3


def test_debug(capsys):
    lib.enable('test:a:b,test:c:*,-examples:*')

    nope = lib.debug('test:a:nope')
    assert callable(nope)
    assert nope == lib.noop

    yay = lib.debug('test:c:yay')
    assert callable(yay)
    yay('should be shown')
    nope('nothing here')
    captured = capsys.readouterr()
    # with capsys.disabled():
    #     print("Here")
    #     print(captured.err)
    #     print("to Here")
    assert "yay 'should be shown' +0.0us" in captured.err
    assert 'nothing here' not in captured.err

    yay('testing', flush=True)
