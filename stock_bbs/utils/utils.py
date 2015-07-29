import traceback

__author__ = 'Simon'


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def print_stack_trace():
        for line in traceback.format_stack():
            print line.strip()
