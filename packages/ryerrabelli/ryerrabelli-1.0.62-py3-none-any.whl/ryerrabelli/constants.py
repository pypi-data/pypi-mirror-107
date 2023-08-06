from typing import List, Set, Dict, Tuple, Any, Optional, Callable, Iterator, Union
# - In Python 3.8 and earlier, the name of the collection type is capitalized, and the type is imported from 'typing'.
# - Examples below
# my_list: List = []
# my_list: list = []  # python 3.9+ only
# - For basic types, like str, int, float, etc, you can always use the lowercase type
# - Source: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html


# All the below variables are defined so they are accessible from the ryerrabelli module
# Lowercase versions kept in for compatibility. However, this are meant to be
# fixed constants (thus style should be capitalized)
FIRST_NAME = "Rahul"
LAST_NAME = "Yerrabelli"
MIDDLE_INITIAL = "S"
NAME = name = FIRST_NAME + " " + LAST_NAME
EMAILS = {}
EMAILS["gmail"] = DEFAULT_EMAIL = EMAIL = GMAIL = "ryerrabelli+python@gmail.com"
USERNAME = username = HANDLE = "ryerrabelli"
GITHUB_BASE = "https://github.com/ryerrabelli/"


# - The below values are not set yet, but will be set during the running of packaging.py, which should be run when any
# module (this module or otherwise) is being setup with setup.py Use Optional[] for values that could be None
# - MutableMapping is equal to dict-like object (Mapping is similar, but doesn't allow __setitem__)
# - Sequence is similar to a list-like object (Iterable is similar but doesn't allow access of length or value at
# specific position)
long_descrip:           Optional[str]       = None
long_descrip_filename:  Optional[str]       = None
requirements:           Optional[List[str]] = None
license_text:           Optional[str]       = None

filenames:              Optional[List[str]] = None
