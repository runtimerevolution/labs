import logging
import os
from typing import List

logger = logging.getLogger(__name__)


def modify_line_in_file(file_path: str, content: List[str], line_number: int):
    logger.info(f"args=(file_path={file_path}, content={content}, line_number={line_number})")
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
