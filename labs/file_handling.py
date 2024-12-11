import logging
import os
from typing import List

logger = logging.getLogger(__name__)


def modify_line_in_file(file_path: str, content: List[str], line_number: int):
    line_number -= 1

    temp_file_path = f"{file_path}.tmp"
    with open(file_path, "r") as original_file, open(temp_file_path, "w") as temp_file:
        for current_line_number, line in enumerate(original_file):
            if current_line_number == line_number:
                for new_line in content:
                    temp_file.write(new_line + "\n")
            else:
                temp_file.write(line)

    # Check if the original file had enough lines
    if current_line_number < line_number:
        print(f"Line number {line_number + 1} does not exist in the file.")
        os.remove(temp_file_path)  # Remove the temp file
        return

    os.replace(temp_file_path, file_path)


def get_file_contents(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            contents = file.read()

            if not contents:
                return ""

            return contents

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.") from e
    except PermissionError as e:
        raise PermissionError(f"Error: You do not have permission to read the file '{file_path}'.") from e
