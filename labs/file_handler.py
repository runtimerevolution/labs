import logging
import os
from typing import List, Union

logger = logging.getLogger(__name__)


def create_file(file_path: str, content: str) -> None:
    logger.info(f"Creating file {file_path}")

    try:
        with open(file_path, "w") as file:
            file.write(content)

    except Exception as e:
        logger.error(f"Error creating file {file_path}: {e}")


def modify_file_line(file_path: str, content: Union[str | List[str]], line_number: int, overwrite=False) -> None:
    logger.info(f"{'Overwriting' if overwrite else 'Modifying'} file {file_path} line {line_number}")

    # Count the number of lines in `content` and ensure it ends in `\n`
    if isinstance(content, list):
        content_lines_count = len(content)
        if content_lines_count > 0 and not content[:-1].endswith("\n"):
            content[:-1] += "\n"

    else:
        content_lines_count = len(content.splitlines())
        if not content.endswith("\n"):
            content += "\n"

    temp_file_path = f"{file_path}.tmp"
    skip_lines = 0
    try:
        with open(file_path, "r") as original_file, open(temp_file_path, "w") as temp_file:
            for current_line_number, line in enumerate(original_file, start=1):
                if current_line_number == line_number:
                    temp_file.writelines(content)
                    if overwrite:
                        skip_lines = content_lines_count

                if skip_lines > 0:
                    skip_lines -= 1
                    continue

                temp_file.write(line)

    except Exception as e:
        logger.error(f"Error modifying file {file_path}: {e}")
        return

    os.replace(temp_file_path, file_path)


def delete_file_line(file_path: str, line_number: int) -> None:
    logger.info(f"Deleting file {file_path} line {line_number}")

    temp_file_path = f"{file_path}.tmp"
    try:
        with open(file_path, "r") as original_file, open(temp_file_path, "w") as temp_file:
            for current_line_number, line in enumerate(original_file, start=1):
                if current_line_number == line_number:
                    continue

                temp_file.write(line)

    except Exception as e:
        logger.error(f"Error deleting lines file {file_path}: {e}")
        return

    os.replace(temp_file_path, file_path)


def get_file_content(file_path: str) -> str:
    try:
        content = ""
        with open(file_path, "r") as file:
            for line_number, line in enumerate(file, start=1):
                content += f"{line_number}: {line}"

        return content

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.") from e

    except PermissionError as e:
        raise PermissionError(f"Error: You do not have permission to read the file '{file_path}'.") from e
