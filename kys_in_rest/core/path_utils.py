import os
from contextlib import contextmanager
from typing import Generator


@contextmanager
def do_in_dir(dir_: str) -> Generator[None, None, None]:
    current_dir = os.getcwd()
    print(f"do_in_dir:enter:{current_dir=}")
    os.chdir(dir_)
    yield
    os.chdir(current_dir)
    print(f"do_in_dir:exit:{current_dir=}")
