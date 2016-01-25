# -*- coding: utf-8 -*-

import sys
import getpass
import argparse


def init_argparser():
    parser = argparse.ArgumentParser(description='Elisa viihde library scripts.')
    parser.add_argument('-u', '--user', help='username')
    parser.add_argument('-p', '--passfile', help='password file')
    parser.add_argument('-v', '--verbose', action='count', help='script verbosity. -v default, -vvv very', default=0)

    return parser


def read_from_file(filename):
    with open(filename, "r") as f:
        # assuming utf-8 encoded file
        return f.read().decode('utf-8')


def read_input(param, question, default=None):
    result = param
    if result is None:
        result = raw_input(question + ': ')
    if result:
        return result.decode(sys.stdin.encoding)
    return default


def read_password(passfileparam, question):
    if passfileparam is not None:
        return read_from_file(passfileparam)
    return getpass.getpass(question + ': ').decode(sys.stdin.encoding)
