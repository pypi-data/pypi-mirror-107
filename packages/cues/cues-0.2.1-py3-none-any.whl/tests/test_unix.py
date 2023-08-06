# -*- coding: utf-8 -*-

"""
tests.test_unix
===============

A testing module for `cues.listen.unix`.
"""

import platform
import select
import sys
try:
    import termios  # pylint: disable=import-error
except ModuleNotFoundError:
    pass
try:
    import tty
except ModuleNotFoundError:
    pass

import pytest

import cues.utils as utils
import cues.listen.unix as unix


@pytest.mark.skipif(platform.system() == 'Windows', reason='OS must not be Windows')
def test_listen(monkeypatch):
    character = 'a'

    def mock_read_return(_):
        return character

    monkeypatch.setattr(sys.stdin, 'fileno', lambda: None)
    monkeypatch.setattr(termios, 'tcgetattr', lambda _: 0)
    monkeypatch.setattr(tty, 'setcbreak', lambda _: None)
    monkeypatch.setattr(unix, 'is_data', lambda: True)
    monkeypatch.setattr(sys.stdin, 'read', mock_read_return)
    monkeypatch.setattr(termios, 'tcsetattr', lambda _, __, ___: 0)

    x = unix.listen()
    assert x == ord(character)


@pytest.mark.skipif(platform.system() == 'Windows', reason='OS must not be Windows')
def test_get_key(monkeypatch):
    character = 'a'

    def mock_read_return(_):
        return character

    monkeypatch.setattr(unix, 'is_data', lambda: True)
    monkeypatch.setattr(sys.stdin, 'read', mock_read_return)

    x = unix.get_key()
    assert x == ord(character)


@pytest.mark.skipif(platform.system() == 'Windows', reason='OS must not be Windows')
def test_get_key_when_key_is_esc(monkeypatch):
    character = '\x1b'

    def mock_read_return(_):
        return character

    monkeypatch.setattr(unix, 'is_data', lambda: True)
    monkeypatch.setattr(sys.stdin, 'read', mock_read_return)

    x = unix.get_key()
    assert x == character


def test_read_pos():
    nums = [10, 6]
    pos = '\x1b[{};{}R'.format(*nums)
    filtered_nums = utils.read_pos(pos)
    assert filtered_nums == nums


@pytest.mark.skipif(platform.system() == 'Windows', reason='OS must not be Windows')
def test_is_data(monkeypatch):
    monkeypatch.setattr(sys.stdin, 'fileno', lambda: None)
    monkeypatch.setattr(select, 'select', lambda _, __, ___, ____: True)

    x = unix.is_data()
    assert x is False
