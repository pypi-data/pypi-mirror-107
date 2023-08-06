"""This module has internal functions/classes that are not useful to access from outside this ryerrabelli module,
but are used by functions within the ryerrabelli module. """

import sys
import os
from io import StringIO


def set_implicit_wait(driver, wait_sec=20):  # seconds
    pass
    driver.implicitly_wait(wait_sec)


def enable_printing() -> None:
    """
    Reference: https://stackoverflow.com/questions/8447185/to-prevent-a-function-from-printing-in-the-batch-console-in-python
    :return:
    :rtype:
    """
    sys.stdout = sys.__stdout__


def disable_printing() -> None:
    """
    Reference: https://stackoverflow.com/questions/8447185/to-prevent-a-function-from-printing-in-the-batch-console-in-python
    :return:
    :rtype:
    """
    sys.stdout = open(os.devnull, "w")


class Capturing(list):
    """
    Reference:
        https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
    Usage:
        with Capturing() as output:
            do_something(my_object)
        # output is now a list containing the lines printed by the function call.

        # Can also be done more than once with results outputted

    Example:
        with Capturing() as output:
            print('hello world')

        print('displays on screen')

        with Capturing(output) as output:  # note the constructor argument
            print('hello world2')

        print('done')
        print('output:', output)

    Example Output:
        displays on screen
        done
        output: ['hello world', 'hello world2']
    """
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

