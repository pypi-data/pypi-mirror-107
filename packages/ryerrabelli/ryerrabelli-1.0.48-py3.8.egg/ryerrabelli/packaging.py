import setuptools
import os
import versioneer

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
    import ryerrabelli as rsy
except ImportError as e:
    from . import constants as rsy





def get_var_from_file(file_choices,
                      func=lambda file: file.read(),
                      default=(None, None),
                      doc_folder="docs"):
    """
    case insensitive
    :param file_choices: Possible filenames for the variable of interest. Case insensitive.
    :type file_choices: list of str
    :param func: function applied to found file to get return value
    :type func: function
    :param default:
    :type default: tuple- 1st element matches expected return type or None, 2nd element filename (str) or None
    :param doc_folder: optional folder to additionally search for, beyond the root folder
    :type doc_folder: str
    :return: tuple of (func applied to the found file, filename of found file)
    :rtype: tuple of (type of func return, str)
    """
    def file_exists(path, use_list=True):
        return path.lower() in rsy.filenames if use_list else os.path.exists(path)
    for filename in file_choices:
        if file_exists(doc_folder + os.sep + filename):
            filename = doc_folder + os.sep + filename
        if file_exists(filename):
            with open(filename, "r") as file:
                return func(file), filename  # found a file, can now break
    return default


def extension_to_format(extension, default=""):
    """
    :param extension: file extension with or without the preceding . i.e. ".md", ".txt"
    :type extension: str
    :param default: default value to return if no description found
    :type default: str
    :return: description of extension type i.e. "text" or "text/markdown"
    :rtype: str
    """
    if extension.startswith("."):
        extension = extension[1:]
    if extension in ["", "txt", "text"]:
        return "text"
    elif extension in ["md"]:
        return "text/markdown"
    else:
        return default


#, path=os.path.abspath(os.curdir)
def get_module_data(module_name, extra_module_data=None, force=False):
    """
    Note- this uses module os to get filenames from a relativ file path. Assuming that this is being run and imported by another program, the file path will be relative to the original program (as intended) and thus will use that python module's filenames (i.e. that module's LICENSE.txt, not this module's)

    The extra_module_data and force functionality are currently untested.

    :param module_name:
    :type module_name: str
    :return: module information that should be passed on to setuptools.setup
    :rtype: dict, need to apply ** operation (i.e. **returned_dict) before sending to setuptools.setup
    """
    if extra_module_data is None:
        extra_module_data = {}
    # Definiton of rsy.filenames has to come before other definitions bc other ones rely on it
    if rsy.filenames is None:
        rsy.filenames = [file.lower() for file in os.listdir()]
        if os.path.exists("docs"):
            rsy.filenames += [("docs" + os.sep + file.lower()) for file in os.listdir("docs")]

    # get_var_from_file(.) input is case insensitive, but most common case styles are shown for illustrative purposes
    if rsy.long_descrip is None or rsy.long_descrip_filename is None:
        rsy.long_descrip, rsy.long_descrip_filename \
            = get_var_from_file(["README", "README.txt", "README.md", "README.rs",
                                 "README-template", "README-template.txt",
                                 "README-template.md", "README-template.rs"],
                                lambda file: file.read(),  # Get string of text
                                default=("", None),
                                )
    if rsy.requirements is None:
        rsy.requirements, _ \
            = get_var_from_file(["requirements", "requirements.txt"],
                                lambda file: [line.strip() for line in file if not line.startswith("#")],  # Get list of (str) requirements, removing lines starting with # aka comments (Note- partial line comments are kept for now for ease)
                                default=([], None),
                                )
    if rsy.license_text is None:
        # Can't name below variable license bc license() returns the python license
        rsy.license_text, _ \
            = get_var_from_file(["LICENSE", "LICENSE.txt", "LICENSE.md", "LICENSE.rtf"],
                                lambda file: file.read(),  # Get string of text
                                default=("", None),
                                )


    # For details on how to document, see:
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#setup-py
    # Calls to versioneer are not to get versions of the ryerrabelli package, but to get the version of the original package.
    standard_module_data = {
        "name": module_name,
        "version": versioneer.get_version(),  # str that includes git commit id per PEP format
        "cmdclass": versioneer.get_cmdclass(),
        "package_dir": {
            "": "src"  # ensures that modules don't have to be referenced from src. first
        },
        "packages": setuptools.find_packages(where="src"),  # list, i.e. [""]
        "url": rsy.GITHUB_BASE + module_name,
        #"license": rsy.license_text,
        "author": rsy.NAME,
        "author_email": rsy.EMAIL,
        "description": "See long description",
        "install_requires": rsy.requirements,  # list of str
        #"long_description": rsy.long_descrip,  # str
        #"long_description_content_type":
        #    extension_to_format(rsy.long_descrip_filename.split(".")[-1]),
        "python_requires": ">=3.6",  # need python 3.6 or higher for f-strings
        "classifiers": [
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            "Environment :: MacOS X",
            "Natural Language :: English"
            ],

    }
    assert force or not any([extra_key in standard_module_data.keys() for extra_key in extra_module_data.keys()]), f"force or not any([extra_key in standard_module_data.keys() for extra_keykey in extra_module_data.keys()]) is wrong for standard_module_data={standard_module_data}, extra_module_data={extra_module_data}, force={force}"

    combined_modula_data = combine_two(standard_module_data, extra_module_data, default=extra_module_data)

    #print(combined_modula_data)
    import json
    print(json.dumps(combined_modula_data, sort_keys=False, indent=4,
                     default=lambda obj: str(obj)  # default is a function called if object is not one of the serializable types
                     ))

    # Operator "**" unpacks dict into named arguments i.e. setup(name=x,version=y, cmdclass=z,...)
    # Save it as a dict first so we can print it out
    return combined_modula_data


def combine_two(obj0, obj1, default=None, default_ind=0):
    if default is None:
        default = obj0 if default_ind == 0 else obj1
    if isinstance(obj0, dict) and isinstance(obj1, dict):
        dict12 = {**obj0, **obj1}  # Combines the dicts. However, obj1's value will have be used if keys are the same (even if the value are combinable objects like lists)
        for conflicted_key in set(obj0).intersection(obj1):  # Go through and try to combine each conflict
            dict12[conflicted_key] = combine_two(
                obj0=obj0[conflicted_key],
                obj1=obj1[conflicted_key],
                default=default[conflicted_key]
            )
        return dict12
    elif isinstance(obj0, list) and isinstance(obj1, list):
        return obj0 + obj1   # Concatenate lists
    else:
        return default


"""
# NOT Finished and NOT Needed right now; combine_two function above is sufficient for now
def combine_all(*objs, default = None, default_ind = 0):
    if default is None:
        default = objs[default_ind]
    if all(isinstance(obj, dict) for obj in objs):
        dict12 = {**obj for obj in objs}  # Combines the dicts. However, obj1 will have be used if keys are the same (even if the value are combinable objects like lists)
        # need to modify below line bc intersection gets only those keys where all dicts conflict; need to also find the keys where only some of the objs conflict
        conflicting_keys = set.intersection(*(set(x) for x in objs))
        for conflicted_key in conflicting_keys:  # Go through and try to combine each conflict
            dict12[conflicted_key] = combine(
                *(objs[conflicted_key]),
                default=default[conflicted_key]
            )
        return dict12
    elif all(isinstance(obj, list) for obj in objs):
        sum = []
        for obj in objs:
            sum += obj
        return sum
    else:
        return default
"""