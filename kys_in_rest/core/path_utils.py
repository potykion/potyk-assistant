import os
from contextlib import contextmanager
from typing import Generator


@contextmanager
def do_in_dir(dir_: str) -> Generator[None, None, None]:
    current_dir = os.getcwd()
    try:
        os.chdir(dir_)
        yield
    finally:
        os.chdir(current_dir)
