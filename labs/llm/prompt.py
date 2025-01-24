import json

INPUT = """
Task description:
    {issue_summary}
"""

INSTRUCTION = """
Based on the task description and the provided system context:
    - Write the code changes required to resolve the task.
    - Ensure that changes are made only within the allowed scope.
"""

OUTPUT = """
You must provide a JSON response in the following format: {json_response}

Operation types explained:
- 'create':
    - Action: This operation is used when the file **does not exist** and needs to be **created from scratch**. It initializes the file with the provided content.
    - Use Case: Used when adding a **completely new file** to the project that **does not currently exist**.

- 'insert':
    - Action: This operation **adds new content** at the **specified line**, pushing subsequent lines down. It **does not modify or replace** any existing content; it simply inserts the new content at the chosen position.
    - Use Case: Used when adding new lines **within an existing file**, either in the middle or before a specific line, without altering any surrounding content.

- 'overwrite':
    - Action: This operation **replaces the content** at the specified line or lines with new content. The existing content at that location is completely erased and replaced with the new content.
    - Use Case: Used when you need to **update** a section of a file, such as modifying a function definition or changing a configuration setting.

- 'delete':
    - Action: This operation **removes content** starting from the specified line or lines. The specified content is deleted entirely, including any text, code, or comments at that location.
    - Use Case: Used when you need to **remove a line or block of lines** from a file, such as deleting a function, comment, or configuration entry.

Ensure operations adhere to the JSON format provided.
"""


JSON_RESPONSE = json.dumps(
    {
        "steps": [
            {
                "type": "Operation type: 'create', 'insert', 'overwrite', or 'delete'",
                "path": "Absolute file path",
                "content": "Content to write (required for 'create', 'insert', or 'overwrite')",
                "line": "Initial line number where the content should be written (or erased if 'delete')",
            }
        ]
    }
)


def get_prompt(issue_summary: str):
    formatted_input = INPUT.format(issue_summary=issue_summary)
    formatted_output = OUTPUT.format(json_response=JSON_RESPONSE)

    prompt = "\n".join([formatted_input, INSTRUCTION, formatted_output])

    return prompt
