import ast

import decorator

from robot.api import logger


def _str_to_data(string):
    try:
        return ast.literal_eval(str(string).strip())
    except Exception:
        return string


@decorator.decorator
def _str_vars_to_data(f, *args, **kwargs):
    args = [_str_to_data(arg) for arg in args]
    kwargs = dict((arg_name, _str_to_data(arg)) for arg_name, arg in kwargs.items())
    result = f(*args, **kwargs)
    return result


class StringPrinter(object):

    def print_string(self, string, start=None, end=None):
        """docstring"""
        if not start:
            start = 0
        if not end:
            end = len(string)
        str_to_print = string[start:end]
        print str_to_print
        logger.info(str_to_print)

class SimpleStringPrinterLibrary(object):
    ROBOT_LIBRARY_SCOPE = 'Global'
    _string_printer = StringPrinter()

    def __init__(self):
        self._string_printer = StringPrinter()

    def get_keyword_names(self):
        """docstring"""
        keywords = [name for name, function in
                    self._string_printer.__dict__.items() if
                    hasattr(function, '__call__')]

        keywords.extend([name for name, function in
                         StringPrinter.__dict__.items() if
                         hasattr(function, '__call__')])
        return keywords

    def __getattr__(self, name):
        func = None
        if name in self._string_printer.__dict__.keys():
            func = getattr(self._string_printer, name)
        elif name in StringPrinter.__dict__.keys():
            func = StringPrinter.__dict__[name]
        if func:
            #return _str_vars_to_data(func)
            return func
        raise AttributeError('Non-existing keyword "{0}"'.format(name))
