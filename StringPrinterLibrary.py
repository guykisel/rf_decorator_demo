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

    def __init__(self, generator=None):
        self.generator = generator

    @classmethod
    def print_string_cls(cls, string, start=None, end=None):
        if not start:
            start = 0
        if not end:
            end = len(string)
        str_to_print = string[start:end]
        print str_to_print
        logger.info(str_to_print)

    def print_string(self, string, start=None, end=None):
        if not start:
            start = 0
        if not end:
            end = len(string)
        str_to_print = string[start:end]
        print str_to_print
        logger.info(str_to_print)


class Generator(object):
    def __init__(self):
        self.providers = []

    def add_provider(self, provider):
        if type(provider) is type:
            provider = provider(self)

        self.providers.insert(0, provider)

        for method_name in dir(provider):
            # skip 'private' method
            if method_name.startswith('_'):
                continue

            faker_function = getattr(provider, method_name)

            if hasattr(faker_function, '__call__') or \
                    isinstance(faker_function, (classmethod, staticmethod)):
                # add all faker method to generator
                self.set_formatter(method_name, faker_function)

    def provider(self, name):
        try:
            lst = [p for p in self.get_providers()
                   if p.__provider__ == name.lower()]
            return lst[0]
        except IndexError:
            return None

    def get_providers(self):
        """Returns added providers."""
        return self.providers

    def format(self, formatter, *args, **kwargs):
        """
        This is a secure way to make a fake from another Provider.
        """
        # TODO: data export?
        return self.get_formatter(formatter)(*args, **kwargs)

    def get_formatter(self, formatter):
        try:
            return getattr(self, formatter)
        except AttributeError:
            raise AttributeError('Unknown formatter "{0}"'.format(formatter))

    def set_formatter(self, name, method):
        """
        This method adds a provider method to generator.
        Override this method to add some decoration or logging stuff.
        """
        setattr(self, name, method)

class Factory(object):
    @classmethod
    def create(cls):
        generator = Generator()
        generator.add_provider(StringPrinter)
        return generator


class StringPrinterLibrary(object):
    ROBOT_LIBRARY_SCOPE = 'Global'
    _string_printer = Factory.create()

    def __init__(self):
        self._string_printer = Factory.create()

    def get_keyword_names(self):
        """docstring"""
        keywords = ['print_string', 'print_string_cls']
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
