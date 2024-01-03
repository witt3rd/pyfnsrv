# Python Server Project

This project uses FastAPI to build a server that accepts Python function submissions, executes them, and returns the results. Below are the key features:

## Features

### Function Submissions

Users can submit Python functions via a POST request to the `/submit/` endpoint. Each submission should include the function code, function name, description, and any dependencies required for the function to run.

### Dependency Management

The server records any function dependencies at the time of submission and installs them using pip. This ensures that the function can execute properly when called.

### Storing Functions

All submitted functions are stored in a SQLite database. The `db.py` file manages all interactions with the database, including saving and querying function records.

### Executing Functions

A request to the `/execute/` endpoint with a named function and argument list triggers the server to retrieve the function from the database, execute it with the provided arguments using Python's built-in `exec()` function, and return the output.

### Listing Functions

A GET request to the `/functions/` endpoint returns a list of all stored functions along with their metadata.

## Future Enhancements

- Better isolation of function execution environments
- Nuanced handling of different versions of the same dependency
- Function updating
- Improved error handling
