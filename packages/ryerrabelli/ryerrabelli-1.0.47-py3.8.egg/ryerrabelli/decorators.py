"""
This module has decorator functions that are useful for accessing from outside the ryerrabelli module
"""
import time
import re
import functools


# Actions in "try:" happen when ryerrabelli module is used to set up any module besides ryerrabelli.
# Actions in "except:" happen when the ryerrabelli module is being setup itself, using the ryerrabelli module.
# Can't use the regular import statements when installing ryerrabelli bc ryerrabelli will not already be installed
# (duh), so can't import it, except by importing it as a relative path To keep the code the same, the renaming of the
# module(s) to "rsy" is helpful. However, for the relative import, we can only have one module named as rsy as we
# need one import statement per module (as opposed to one import statement for the entire package as done when
# ryerrabelli is used external code). Fortunately, each file that imports ryerrabelli only requires functions from
# one other module. The setup.py file only needs to import ryerrabelli functions that are in main.py (doesn't need
# any functions in utils.py) and main.py only needs to import functions from util.py
# ***NOTE: Above message is present in multiple files. Update text in all if comment is changed.
try:
    from ryerrabelli import utils
except ImportError as e:
    from . import utils

#from ryerrabelli import utils



def analyze_function(print_args: bool = True, time_fmt: str = "0.4f", do: bool = True, is_command: bool = True):
    """This is a decorator function used to nicely time functions as well as print out their inputs.
    # https://stackoverflow.com/questions/52214720/whether-the-return-value-of-a-function-modified-by-python-decorator-can-only-be
    # https://www.geeksforgeeks.org/decorator-to-print-function-call-details-in-python/
    The arguments to the outer "analyze_function(.)" function are arguments to the decorator (like @analyze_function(do=False) )
    Structurally, this function is a function of a function because this was needed in order the decorator to work for any function (with any number of arguments, including args/kwargs)
    :param print_args:
    :type print_args: bool
    :param time_fmt: format of time
    :type time_fmt: str
    :param do: Making this false is the same as not calling this function. Having it as a variable makes the syntax sometimes easier.
    :type do: bool
    :param is_command: The is_commands variable is for functions like "run_command(commands, args,...)" where commands=["git"] and args=["describe","--tags"] so that the output into bash/zsh is like "git describe --tags"
    :type is_command: bool
    :return:
    :rtype:
    """

    def my_decorator(func: callable):
        """

        :param func: The function being wrapped. The "@" syntactic sugar automatically puts this as an argument.
        :type func: function
        :return:
        :rtype:
        """
        # Getting the argument names of the called function
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """

            :param args: the positional arguments to the decorated function
            :type args: list
            :param kwargs: the named arguments to the decorated function
            :type kwargs: list
            :return: same as the decorated function
            :rtype: same as the decorated function
            """
            if not do:
                return func(*args, **kwargs)

            if is_command:
                print(" ".join([" ".join(args[0])] + args[1]))

            t0 = time.time()
            try:
                return func(*args, **kwargs)
            finally:  # "finally" runs no matter what - whether error is thrown or not, even if return keyword is given
                t1 = time.time()
                # There also is the func.__code__ var, but that is too much to print nicely
                if print_args:
                    # print(f"Took {t1 - t0:{time_fmt}} sec to run: {func.__name__}({', '.join('% s = % r' % entry for entry in zip(argnames, args[:len(argnames)]))} ), args = {list(args[len(argnames):])}, kwargs = {kwargs}")
                    print(f"Took {t1 - t0:{time_fmt}} sec to run: {func.__name__}" +
                          f"({', '.join('% s=% r' % entry for entry in zip(arg_names, args[:len(arg_names)]))} ), args = {list(args[len(arg_names):])}, kwargs = {kwargs}")
                else:
                    print(f"Took {t1 - t0:{time_fmt}} sec to run '{func.__name__}'")

        return wrapper

    return my_decorator


def display_unittest_as_formatted(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        # True for print at the end
        # None for no printing
        # False for regular printing behavior
        intercept_function_prints = False

        headers = {
            "Function name": ":   \t",
            "Result": ":          \t",
            "Prints (if any)": ": \t",
            "Returned": ":        \t",
        }

        def align(text, obj=None):
            header_spacing = headers.get(text)
            if obj is None:
                # Return a tuple
                # 2nd element in tuple represents  amount of indent needed for subsequent prints
                # The regex replaces any non-space elements with a space
                # Use regex instead of just " " * len bc header_spacing could include tabs, which are one element,
                # but visually show up as multiple elements
                #return text + header_spacing, " " *  len(text) + (" " + header_spacing[1:])
                #return text + header_spacing, " " * (len(text) + len(header_spacing))
                return           text  +                       header_spacing, \
                       " " * len(text) + re.sub(r"[^\s]", " ", header_spacing)
            else:
                return           text  +                       header_spacing + str(obj)

        print(align("Function name", f.__name__))
        try:
            if intercept_function_prints is None:
                utils.disable_printing()
            else:
                to_print_left, to_print_right = align("Prints (if any)")
                print(to_print_left)

            if intercept_function_prints:
                with utils.Capturing() as outputs:
                    to_return = f(*args, **kwargs)
                for output in outputs:
                    #print("\t", output)
                    pass
                    print(to_print_right, output)
            else:
                to_return = f(*args, **kwargs)
                # Automatic printing within the function

            if intercept_function_prints is None:
                utils.enable_printing()
            if to_return is None:
                print(align("Result", "No error!"))
            else:
                #print("Result: \tNo error! Returned: \t", to_return)
                print(align("Result", "No error!"))
                #print(align("Returned", to_return))

            print()
            print("##############################")
            return to_return
        except Exception as e:
            print(align("Result"), "Error!")
            print()
            raise e
    return wrapped

