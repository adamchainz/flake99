# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from flake99 import do_fixes


def test_passthrough():
    assert do_fixes('1\n') == '1\n'


def test_trailing_spaces_removed():
    assert do_fixes('1  \n') == '1\n'


def test_trailing_tabs_removed():
    assert do_fixes('1\t\n') == '1\n'


def test_trailing_spaces_comment_removed():
    assert do_fixes('1  # a  \n') == '1  # a\n'


def test_trailing_tabs_comment_removed():
    assert do_fixes('1  # a\t\n') == '1  # a\n'


def test_trailing_blank_lines_removed():
    # W391
    assert do_fixes('1\n\n') == '1\n'


def test_trailing_blank_line_added():
    # W391
    assert do_fixes('1') == '1\n'
