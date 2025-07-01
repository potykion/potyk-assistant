import os
from contextlib import contextmanager


@contextmanager
def do_in_dir(dir_: str):
    current_dir = os.getcwd()
    os.chdir(dir_)
    yield
    os.chdir(current_dir)
