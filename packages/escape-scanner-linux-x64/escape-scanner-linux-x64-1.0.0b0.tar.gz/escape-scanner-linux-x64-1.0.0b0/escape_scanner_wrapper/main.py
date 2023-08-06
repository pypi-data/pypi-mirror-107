"""Wrapper to execute the Scanner in Python"""

import sys
import os
from importlib import resources

from escape_scanner_wrapper import static


def execute(*args) -> None:
    """Execute scanner as imported package"""
    # This is how we open static files inside packages in Python
    with resources.path(static, 'escape-scanner') as scanner_path:
        cmd = [str(scanner_path.resolve())]

    cmd += args
    cmd = ' '.join(cmd)

    os.environ['LC_ALL'] = 'C.UTF-8'
    os.environ['LANG'] = 'C.UTF-8'

    print(cmd)

    os.system(cmd)  # returns the exit status


def main() -> None:
    """Execute scanner as CLI"""
    if len(sys.argv) > 1:
        execute(*sys.argv[1:])
    else:
        execute()
