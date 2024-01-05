# System imports
import os
import datetime
import shelve

# Third-party imports
import chromadb
from dotenv import load_dotenv

# Local imports
from app.models import FunctionDef, FunctionSummary

#

load_dotenv()

DB_DIR = os.getenv("DB_DIR", "./db")
FN_DB_NAME = os.getenv("FN_DB_NAME", "fns.db")
FN_DB_PATH = os.path.join(DB_DIR, FN_DB_NAME)
IDX_COL_NAME = os.getenv("IDX_COL_NAME", "fns")

#


def _index_add_function(function: FunctionDef) -> None:
    client = chromadb.PersistentClient(path=DB_DIR)
    col = client.get_or_create_collection(name=IDX_COL_NAME)
    col.add(
        ids=function.name,
        documents=function.description,
    )


def _index_query_functions(
    query: str,
    n: int = 10,
) -> list[FunctionSummary]:
    client = chromadb.PersistentClient(path=DB_DIR)
    col = client.get_or_create_collection(name=IDX_COL_NAME)
    result = col.query(query_texts=query, n_results=n)
    names = result["ids"][0]
    functions = result["documents"][0]
    return [
        FunctionSummary(
            name=name.strip(),
            description=description.strip(),
        )
        for name, description in zip(names, functions)
    ]


def db_add_function(function: FunctionDef) -> bool:
    """
    Add a function to the database.

    Args:
        function (FunctionDef): The function to be added.

    Returns:
        bool: True if the function is added as a new entry, False if it updates an existing entry.
    """
    with shelve.open(FN_DB_PATH) as db:
        clean_fn = function.model_copy(
            update={
                "name": function.name.strip(),
                "description": function.description.strip(),
            }
        )
        existing_function = db.get(clean_fn.name)
        if existing_function:
            clean_fn.updated_at = datetime.datetime.utcnow()
        else:
            clean_fn.created_at = datetime.datetime.utcnow()
        db[clean_fn.name] = clean_fn
    _index_add_function(clean_fn)
    return existing_function is None


def db_get_function(name: str) -> FunctionDef | None:
    """
    Get a function from the database.

    Args:
        name (str): The name of the function to get.

    Returns:
        FunctionDef | None: The function if it exists, None otherwise.
    """
    with shelve.open(FN_DB_PATH) as db:
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
    with shelve.open(FN_DB_PATH) as db:
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
    with shelve.open(FN_DB_PATH) as db:
        functions = list(db.values())
        return [
            FunctionSummary(
                name=f.name.strip(),
                description=f.description.strip(),
            )
            for f in functions
        ]


def db_get_all_functions() -> list[FunctionDef]:
    """
    Get all functions from the database.

    Returns:
        list[FunctionDef]: A list of all functions.
    """
    with shelve.open(FN_DB_PATH) as db:
        functions = list(db.values())
        return functions


def db_find_functions(query: str, n: int = 10) -> list[FunctionSummary]:
    """
    Find functions from the database.

    Args:
        query (str): The query string.
        n (int, optional): The number of results to return. Defaults to 10.

    Returns:
        list[FunctionSummary]: A list of functions.
    """
    return _index_query_functions(query, n=n)


if __name__ == "__main__":
    functions = db_get_all_functions()
    for function in functions:
        _index_add_function(function)
    print(_index_query_functions("greeting", n=1))
