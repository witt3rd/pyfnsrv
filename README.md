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

## Running the Server

To run the server, first install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

Then, run the server using the provided `run.sh` script:

```sh
./run.sh
```

## Testing the Server

### Submitting a Function

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/functions/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "my_function",
  "code": "import numpy as np\nimport pandas as pd\n\ndef generate_random_dataframe(count, min_value, max_value):\n    data = pd.DataFrame({'\''A'\'': np.random.uniform(min_value, max_value, count)})\n    return data\n\ndef calculate_mean(dataframe, column):\n    return np.mean(dataframe[column])\n\ndef my_function(count: int, min_value: float, max_value: float) -> float:\n    data = generate_random_dataframe(count, min_value, max_value)\n    mean = calculate_mean(data, '\''A'\'')\n    return mean\n",
  "description": "A function that calculates the mean of a column in a pandas DataFrame using numpy",
  "dependencies": [
    "numpy",
    "pandas"
  ],
  "args": {
    "count": "int",
    "min_value": "float",
    "max_value": "float"
  }
}'
```

### Listing Functions

```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/functions/' \
  -H 'accept: application/json'
```

### Executing a Function

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/execute/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "my_function",
  "args": {"count": 10, "min_value": 0.0, "max_value": 100.0}
}'
```
