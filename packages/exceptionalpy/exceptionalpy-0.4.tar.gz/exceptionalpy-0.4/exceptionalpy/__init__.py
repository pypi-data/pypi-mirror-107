#  MIT License
#
#  Copyright (c) 2021 Pascal Eberlein
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import pprint
import sys
import traceback as tb
import time


class BaseNotifier(object):
    def send(self, data: dict) -> bool:
        """
        send data
        :param data: dict
        :return: True if sending was successful, else False
        """
        raise NotImplementedError("This should be overridden")


class Handler(object):
    _orig_unraisablehook = None

    notifier: BaseNotifier = None

    def __init__(self, init: bool = True, verbose: bool = False):
        """

        :param init: override exception hooks right now
        :param verbose: print information about timing and exceptions to cli
        """
        self.verbose = verbose
        if init:
            self.init()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deinit()

    def init(self) -> None:
        """
        overrides
            sys.excepthook
            sys.unraisablehook
        with
            self.custom_excepthook
            self.custom_unraisablehook
        and stores the old value of
            sys.unraisablehook
        in
            self._orig_unraisablehook
        :return:
        """
        if self.verbose:
            print("Replacing exception hooks")
        sys.excepthook = self.custom_excepthook
        self._orig_unraisablehook = sys.unraisablehook
        sys.unraisablehook = self.custom_unraisablehook

    def deinit(self) -> None:
        """
        sets
            sys.excepthook
            sys.unraisablehook
        back to its original values
        :return:
        """
        if self.verbose:
            print("Setting original exception hooks")
        sys.excepthook = sys.__excepthook__
        sys.unraisablehook = self._orig_unraisablehook

    def traceback2json(self, traceback) -> dict:
        """
        convert a traceback to json
        prints the traceback if self.verbose is True
        :param traceback:
        :return:
        """
        r = {
            "frames": []
        }
        e = tb.extract_tb(traceback)
        for f in e:
            r["frames"].append({
                "filename": f.filename,
                "line_number": f.lineno,
                "name": f.name,
                "line": f.line
            })

        if self.verbose:
            pprint.pprint(r)

        return r

    def show_exception(self, etype, value, traceback):
        """
        shows the current exception information in cli if self.verbose is True
        :param etype:
        :param value:
        :param traceback:
        :return:
        """
        if not self.verbose:
            return

        print(10 * "-" + " EXCEPTION " + 10 * "-")
        print(etype, value)
        for line in tb.format_exception(etype, value, traceback):
            print(line)
        self.traceback2json(traceback)  # todo remove
        print(31 * "-")
        print()

    def show_timeit(self, fn, begin, end):
        """
        print information about timing if self.verbose is True
        :param fn:
        :param begin:
        :param end:
        :return:
        """
        if not self.verbose:
            return
        ns = end - begin
        ms = ns / 1000000
        s = ms / 1000
        print(fn.__name__, "completed in", ns, "ns |", ms, "ms |", s, "s")

    def custom_excepthook(self, etype, value, traceback) -> None:
        """
        calls
            self.show_exception
            self.notifier.send if self.notifier is not None

        :param etype:
        :param value:
        :param traceback:
        :return:
        """
        self.show_exception(etype, value, traceback)

        if self.notifier is not None:
            self.notifier.send(self.traceback2json(traceback))

    def custom_unraisablehook(self, etype, value, traceback, msg, obj):
        """
        calls
            self.show_exception
        :param etype:
        :param value:
        :param traceback:
        :param msg:
        :param obj:
        :return:
        """
        self.show_exception(etype, value, traceback)

    def handle_exception(self, exception, fn, *args, **kwargs) -> None:
        """
        gets
            sys.exc_info
        and calls
            self.show_exception
        with the retrieved values

        :param exception:
        :param fn:
        :param args:
        :param kwargs:
        :return:
        """
        etype, ex, tb = sys.exc_info()
        self.show_exception(etype, ex, tb)

    def handle_timeit(self, fn, begin, end, *args, **kwargs):
        """
        calls
            self.show_timeit

        :param fn:
        :param begin:
        :param end:
        :param args:
        :param kwargs:
        :return:
        """
        self.show_timeit(fn, begin, end)


class Replacer(Handler):
    classes = {}

    def attach(self):
        def wrapper(cls):
            self.classes[cls.__name__] = cls
            return cls
        return wrapper


exceptionalpy_handler: Handler = Handler(False, False)


def _timeit(fn: callable, *args, **kwargs) -> int:
    """
    measures the time it takes in nanoseconds until a function completes running
    :param fn: callable, the function to measure
    :param args:
    :param kwargs:
    :return:
    """
    b = time.time_ns()
    r = fn(*args, **kwargs)
    e = time.time_ns()
    exceptionalpy_handler.handle_timeit(fn, b, e, *args, **kwargs)
    return r


def _catch(fn: callable, *args, **kwargs):
    """
    try to execute a function and return the functions return value
    or, if there is an exception, call
        handle_exception
    on the current instance of
        exceptional_handler

    :param fn:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        exceptionalpy_handler.handle_exception(e, fn, *args, **kwargs)
        pass


def catch():
    """
    decorator
    catches an exception if one occurs
    and forwards it to the global exception handler
    :return:
    """
    def decorator(fn):
        def wrapper(*args, **kwargs):
            return _catch(fn, *args, **kwargs)
        return wrapper
    return decorator


def timeit():
    """
    decorator
    measures how long a function takes to execute
    and forwards it to the global exception handler
    :return:
    """
    def decorator(fn):
        def wrapper(*args, **kwargs):
            return _timeit(fn, *args, *kwargs)
        return wrapper
    return decorator


def catch_timeit():
    """
    decorator
    catches an exception if one occurs
    measures how long a function takes to execute
    and forwards that information to the global exception handler
    :return:
    """
    def decorator(fn):
        @ex()
        def wrapper(*args, **kwargs):
            return _timeit(fn, *args, **kwargs)
        return wrapper
    return decorator


ex = catch
ti = timeit
exti = catch_timeit


def initialize(cls, *args, **kwargs):
    """
    initialize global exceptionalpy_handler instance with given cls, args and kwargs
    :param cls:
    :param args:
    :param kwargs:
    :return:
    """
    global exceptionalpy_handler
    exceptionalpy_handler = cls(*args, **kwargs)


__all__ = ["Handler", "BaseNotifier",
           "exceptionalpy_handler",
           "catch", "timeit", "catch_timeit",
           "ex", "ti", "exti",
           "initialize"]
