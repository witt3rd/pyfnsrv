# System imports
import os
import datetime
import shelve

# Third-party imports
from dotenv import load_dotenv

# Local imports
from app.models import FunctionDef, FunctionSummary

#

load_dotenv()

DB_PATH = os.getenv("DB_PATH")

#


def db_add_function(function: FunctionDef) -> bool:
    """
    Add a function to the database.

    Args:
        function (FunctionDef): The function to be added.

    Returns:
        bool: True if the function is added as a new entry, False if it updates an existing entry.
    """
    with shelve.open(DB_PATH) as db:
        existing_function = db.get(function.name)
        if existing_function:
            function.updated_at = datetime.datetime.utcnow()
            db[function.name] = function
            return False
        else:
            function.created_at = datetime.datetime.utcnow()
            db[function.name] = function
            return True


def db_get_function(name: str) -> FunctionDef | None:
    """
    Get a function from the database.

    Args:
        name (str): The name of the function to get.

    Returns:
        FunctionDef | None: The function if it exists, None otherwise.
    """
    with shelve.open(DB_PATH) as db:
        function = db.get(name)
        return function


def db_get_functions(names: list[str]) -> list[FunctionDef]:
    """
    Get a list of functions from the database.

    Args:
        names (list[str]): A list of function names to get.

    Returns:
        list[FunctionDef]: A list of functions.

    Raises:
        ValueError: If any of the names are missing in the database.
    """
    with shelve.open(DB_PATH) as db:
        functions = [db.get(name) for name in names]
        if None in functions:
            missing_names = [
                name for name, function in zip(names, functions) if function is None
            ]
            raise ValueError(
                f"The following names are missing in the database: {missing_names}"
            )
        return functions


def db_get_all_function_summaries() -> list[FunctionSummary]:
    """
    Get all function summaries from the database.

    Returns:
        list[FunctionSummary]: A list of all functions.

    Raises:
        FileNotFoundError: If the database file is not found.
    """
    with shelve.open(DB_PATH) as db:
        functions = list(db.values())
        return [
            FunctionSummary(
                name=f.name,
                description=f.description,
            )
            for f in functions
        ]


def db_get_all_functions() -> list[FunctionDef]:
    """
    Get all functions from the database.

    Returns:
        list[FunctionDef]: A list of all functions.
    """
    with shelve.open(DB_PATH) as db:
        functions = list(db.values())
        return functions
