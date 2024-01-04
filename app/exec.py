# System imports
import subprocess

# Local imports
from app.db import db_get_functions
from app.models import Arg, FunctionDef

#


def exec_install_dependencies(dependencies: list[str]) -> None:
    """
    Install the specified dependencies using pip.

    Args:
        dependencies (list[str]): A list of dependencies to be installed.

    Raises:
        CalledProcessError: If the installation process fails.

    Returns:
        None
    """
    for dependency in dependencies:
        subprocess.check_call(["python3", "-m", "pip", "install", dependency])


def exec_execute_code(
    fn: FunctionDef,
    args: list[Arg] | None = None,
) -> any:
    """
    Executes the given function `fn` with the provided arguments `args`.

    Args:
        fn (FunctionDef): The function to be executed.
        args (list[Arg]): The arguments to be passed to the function.

    Returns:
        any: The result of executing the function.
    """

    def _include_dependent_functions(_fn, _namespace) -> None:
        for dep_fn in db_get_functions(_fn.fn_dependencies):
            _include_dependent_functions(dep_fn, _namespace)
        exec(_fn.code, _namespace)

    namespace = {}
    _include_dependent_functions(fn, namespace)
    actual_args = {arg.name: arg.value for arg in args} if args else None
    return namespace[fn.name](**actual_args) if actual_args else namespace[fn.name]()
