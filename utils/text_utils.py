import json
import inspect


def output_to_json(data: str) -> str:
    """
    Convert python to JSON string.
    """
    return json.dumps(data)


def remove_white_spaces(string: str) -> str:
    """
    Removes extra white spaces from a string.
    """
    return " ".join(string.split())


def load_json_file(json_file: str) -> dict:
    """
    Load JSON file.
    """
    with open(json_file, encoding="utf-8") as f:
        return json.load(f)


def get_docstring_summary_and_description(func):
    """
    Extracts the summary and description from a function's docstring.

    Args:
        func (function): The function whose docstring is to be parsed.

    Returns:
        tuple: A tuple containing the summary and description.
    """
    docstring = inspect.getdoc(func)
    if not docstring:
        return "", ""

    lines = docstring.split("\n")
    summary = lines[0]
    description = "\n".join(lines[1:]).strip()
    return summary, description
