from pyhere import here
from pathlib import PosixPath
from typing import (
    Union,
    Callable,
    Iterable,
    Mapping
)

def __make_dir_function(
    dirname: Union[str, Iterable[str]]
) -> Callable[..., PosixPath]:
    """Generate a fucntion that converts a string or iterable of strings into
    a path relative to the project directory.

    Args:
        dirname: Name of the subdirectories to extend the path of the main
            project.
            If an iterable of strings is passed as an argument, then it is
            collapsed to a single steing with anchors dependent on the
            operating system.

    Returns:
        A function that returns the path relative to a directory that can
        receive `n` number of arguments for expansion.
    """

    def dir_path(*args) -> PosixPath:
        if type(dirname) == str:
            return here(dirname, *args)
        else:
            return here(*dirname, *args)

    return dir_path

def __generate_default_subdirs() -> None:
    """Generate functions to access the path of default subdirectories.
    """

    dir_types = [
        ["data"],
        ["data", "raw"],
        ["data", "processed"],
        ["data", "interim"],
        ["data", "external"],
        ["notebooks"],
        ["reports"],
        ["reports", "figures"],
        ["src"]
    ]

    for dir_type in dir_types:
        dir_var = '_'.join(dir_type) + "_dir"
        exec(f"global {dir_var}; {dir_var} = __make_dir_function({dir_type})")

__generate_default_subdirs()