import subprocess


def install_dependencies(dependencies: list[str]):
    for dependency in dependencies:
        subprocess.check_call(["python3", "-m", "pip", "install", dependency])


def execute_code(code: str, name: str, args: dict[str, any]):
    namespace = {}
    exec(code, namespace)

    return namespace[name](**args)


if __name__ == "__main__":
    install_dependencies(["numpy", "pandas"])

    code = """
import numpy as np
import pandas as pd

def generate_random_dataframe(count, min_value, max_value):
	data = pd.DataFrame({'A': np.random.uniform(min_value, max_value, count)})
	return data

def calculate_mean(dataframe, column):
	return np.mean(dataframe[column])

def my_function(
	count: int,
    min_value: float,
    max_value: float,
    ) -> float:
	data = generate_random_dataframe(count, min_value, max_value)
	mean = calculate_mean(data, 'A')
	return mean
"""

    args = {"count": 10, "min_value": 0.0, "max_value": 100.0}
    result = execute_code(code, "my_function", args)
    print(result)
