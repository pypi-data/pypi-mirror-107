import sys
import os
from importlib import resources

from escape_scanner_wrapper import static


def execute(*args):
    # This is how we open static files inside packages in Python
    with resources.path(static, 'escape-scanner') as scanner_path:
        cmd = [str(scanner_path.resolve())]

    cmd += args
    cmd = ' '.join(cmd)
    print(cmd)

    os.system(cmd)  # returns the exit status


def main():
    if len(sys.argv) > 1:
        execute(*sys.argv[1:])
    else:
        execute()
