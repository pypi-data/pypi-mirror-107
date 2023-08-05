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
    def send(self, data: dict):
        pass


class Handler(object):
    _orig_unraisablehook = None
    notifier: BaseNotifier = None

    def __init__(self, init: bool = True, verbose: bool = False):
        self.verbose = verbose
        if init:
            self.init()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deinit()

    def init(self) -> None:
        if self.verbose:
            print("Replacing exception hooks")
        sys.excepthook = self.custom_excepthook
        self._orig_unraisablehook = sys.unraisablehook
        sys.unraisablehook = self.custom_unraisablehook

    def deinit(self) -> None:
        if self.verbose:
            print("Setting original exception hooks")
        sys.excepthook = sys.__excepthook__
        sys.unraisablehook = self._orig_unraisablehook

    def traceback2json(self, traceback) -> dict:
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
        ns = end - begin
        ms = ns / 1000000
        s = ms / 1000
        print(fn.__name__, "completed in", ns, "ns |", ms, "ms |", s, "s")

    def custom_excepthook(self, etype, value, traceback) -> None:
        self.show_exception(etype, value, traceback)

        if self.notifier is not None:
            self.notifier.send(self.traceback2json(traceback))

    def custom_unraisablehook(self, etype, value, traceback, msg, obj):
        self.show_exception(etype, value, traceback)

    def handle_exception(self, exception, fn, *args, **kwargs) -> None:
        etype, ex, tb = sys.exc_info()
        self.show_exception(etype, ex, tb)

    def handle_timeit(self, fn, begin, end, *args, **kwargs):
        self.show_timeit(fn, begin, end)


exceptionalpy_handler: Handler = Handler(False, False)


def timeit(fn, *args, **kwargs):
    b = time.time_ns()
    r = fn(*args, **kwargs)
    e = time.time_ns()
    exceptionalpy_handler.handle_timeit(fn, b, e, *args, **kwargs)
    return r


def catch(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        exceptionalpy_handler.handle_exception(e, fn, *args, **kwargs)
        pass


def ex():
    def decorator(fn):
        def wrapper(*args, **kwargs):
            return catch(fn, *args, **kwargs)
        return wrapper
    return decorator


def ti():
    def decorator(fn):
        def wrapper(*args, **kwargs):
            return timeit(fn, *args, *kwargs)
        return wrapper
    return decorator


def exti():
    def decorator(fn):
        @ex()
        def wrapper(*args, **kwargs):
            return timeit(fn, *args, **kwargs)
        return wrapper
    return decorator


class Rescuer(Handler):
    classes: list = None

    def __init__(self, init: bool = True, verbose: bool = False):
        Handler.__init__(self, init, verbose)


__all__ = ["Handler", "BaseNotifier",
           "exceptionalpy_handler",
           "ex", "ti", "exti"]
