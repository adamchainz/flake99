# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from redbaron import RedBaron


def main():
    for filename in sys.argv[1:]:
        fix_file(filename)


def fix_file(filename):
    with open(filename, 'r') as fp:
        code_str = fp.read()

    fixed_code_str = do_fixes(code_str)

    with open(filename, 'w') as fp:
        fp.write(fixed_code_str)


def do_fixes(code_str):
    baron = RedBaron(code_str)
    fix_trailing_whitespace(baron)
    return baron.dumps()


def fix_trailing_whitespace(baron):
    # The only formatting that can precede an EndlNode seems to be trailing
    # whitespace, so remove it all
    for endl in baron.find_all('EndlNode'):
        if endl.formatting:
            endl.formatting = []

    # In Python, comments always end the line, and the trailing whitespace is
    # parsed into the comment, so remove it
    for comment in baron.find_all('CommentNode'):
        comment.value = comment.value.rstrip(' \t\v')


if __name__ == '__main__':
    main()
