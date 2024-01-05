# System imports
from typing import Dict, Any

# Third-party imports
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

# Local imports
from app.db import (
    db_add_function,
    db_get_function,
    db_get_all_functions,
    db_get_all_function_summaries,
    db_find_functions,
)
from app.exec import exec_execute_code, exec_install_dependencies
from app.models import Arg, FunctionDef, FunctionSummary, Query

#

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],  # Allow this origin
    allow_credentials=True,  # Allow cookies to be sent with requests
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

#


@app.post("/functions/")
def submit_function(fn: FunctionDef) -> Response:
    """
    Submit a function definition and process it.

    Args:
        fn (FunctionDef): The function definition to submit.

    Returns:
        Response: The HTTP response indicating the status of the submission.
    """
    is_new = db_add_function(fn)
    exec_install_dependencies(fn.pkg_dependencies)
    if is_new:
        return Response(status_code=201)
    else:
        return Response(status_code=200)


@app.get("/functions/")
def get_functions() -> list[FunctionDef]:
    """
    Retrieve all functions.

    Returns:
        list[FunctionDef]: A list of FunctionDef objects representing the functions.
    """
    fns = db_get_all_functions()
    return fns


@app.get("/functions/summaries")
def get_functions_summaries() -> list[FunctionSummary]:
    """
    Retrieve summaries of all functions.

    Returns:
        list[FunctionSummary]: A list of function summaries.
    """
    summaries = db_get_all_function_summaries()
    return summaries


@app.get("/functions/{name}")
def get_function(name: str) -> FunctionDef:
    """
    Retrieve a function by name.

    Args:
        name (str): The name of the function.

    Returns:
        FunctionDef: The function definition.
    """
    fn = db_get_function(name)
    if fn is None:
        return Response(status_code=404)
    print(fn)
    return fn


@app.post("/functions/search")
def search_functions(query: Query) -> list[FunctionSummary]:
    """
    Searches for functions based on the provided query string and number of results.

    Args:
        query (Query): The Query object containing the search string and number of results.

    Returns:
        Response: The response object indicating the status code and search results.
    """
    results = db_find_functions(query.query, query.n_results)
    return results


@app.post("/functions/{name}/execute/")
def execute_function(
    name: str,
    args: list[Arg] | None = None,
) -> Dict[str, Any]:
    """
    Executes a function based on the provided FunctionExec object.

    Args:
        name (str): The name of the function.
        args (Arg): The Arg object containing the function arguments.

    Returns:
        Response: The response object indicating the status code and execution result.
    """
    fn_def = db_get_function(name)
    if fn_def is None:
        return Response(status_code=404)
    exec_result = exec_execute_code(
        fn=fn_def,
        args=args,
    )
    return exec_result
