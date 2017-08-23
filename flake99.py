# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from redbaron import RedBaron
from redbaron.nodes import EndlNode


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
    document = Document(baron)
    for checker in checkers:
        checker.fix(document)
    return document.baron.dumps()


class Document(object):
    """
    Represents a full Python file, includes
    """
    def __init__(self, baron):
        # RedBaron instance
        self.baron = baron


class Checker(object):

    def check(self, document):
        """
        Should return a list of Problem
        """
        return []

    def fix(self, document):
        """
        May make any changes to document.baron to make it look right
        """
        pass


class Problem(object):
    def __init__(self, lineno, charno, message):
        self.lineno = lineno
        self.charno = charno
        self.message = message


class TrailingWhitespaceChecker(Checker):

    def fix(self, document):
        # The only formatting that can precede an EndlNode seems to be trailing
        # whitespace, so remove it all
        for endl in document.baron.find_all('EndlNode'):
            if endl.formatting:
                endl.formatting = []

        # In Python, comments always end the line, and the trailing whitespace is
        # parsed into the comment, so remove it
        for comment in document.baron.find_all('CommentNode'):
            comment.value = comment.value.rstrip(' \t\v')


class TrailingBlankLineChecker(Checker):
    def fix(self, document):
        baron = document.baron
        if not isinstance(baron.node_list[-1], EndlNode):
            endl = RedBaron('\n').node_list[0]
            baron.node_list.append(endl)

        while isinstance(baron.node_list[-2], EndlNode):
            del baron.node_list[-2]


checkers = [
    TrailingWhitespaceChecker(),
    TrailingBlankLineChecker(),
]


if __name__ == '__main__':
    main()
