"""Wrapper to execute the Scanner in Python"""
import sys
import os
from importlib import resources
from escape_scanner_wrapper import static


def execute(*args):
    """Execute scanner as imported package"""
    with resources.path(static, 'escape-scanner') as scanner_path:
        full_path = str(scanner_path.resolve())
        cmd = [full_path]
    cmd += args
    cmd = ' '.join(cmd)
    print(cmd)
    os.system(f'chmod +x {full_path}')
    os.system(cmd)


def main():
    """Execute scanner as CLI"""
    if len(sys.argv) > 1:
        execute(*sys.argv[1:])
    else:
        execute()
