import os
import sys
from argparse import ArgumentParser

# Remove "" and current working directory from the first entry of sys.path
if sys.path[0] in ("", os.getcwd()):
    sys.path.pop(0)

from hej.files.ops import difference


def args_difference(args=None):
    parser = ArgumentParser(description="a/ - b/")
    parser.add_argument("a", type=str,
                        help="with elements in the set")
    parser.add_argument("b", type=str,
                        help="with elements not in the set")
    parser.add_argument("-o", "--out", type=str, default=None,
                        help="output dir, default is `{a}_diff`")
    parser.add_argument("-i", "--suffixes", type=str, default=None,
                        help="such as '.txt,.jpg,.jpeg'")
    parser.add_argument("-f", "--flatten", action="store_true",
                        help="flatten or not")
    args = parser.parse_args(args=args)

    kw = vars(args)
    return kw


help_doc_str = """
Options:

positional arguments:
    command
        a-b
"""


def _main(args=None):
    if args is None:
        args = sys.argv[1:]

    if len(args) >= 1:
        task, *args = args
    else:
        task, *args = ["--help"]

    if task == "a-b":
        kw = args_difference(args)
        print(f"kwargs: {kw}")
        return difference(**kw)
    elif task == "-h" or task == "--help":
        print("usage: python -m hej.files command ...\n")
    else:
        print(f"unimplemented command: {task}\n")

    return help_doc_str


# develop:
# PYTHONPATH=$(pwd):$(pwd) python hej/files ...
# runtime:
# python -m hej.files ...
if __name__ == "__main__":
    print(_main())
    sys.exit(0)
