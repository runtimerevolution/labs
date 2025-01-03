import json

INPUT = """
Task description:
    {issue_summary}
"""

INSTRUCTION = """
Based on the task description and the provided system context:
    - Write the Python code changes required to resolve the task.
    - Ensure that changes are made only within the allowed scope.
"""

OUTPUT = """
You must provide a JSON response in the following format: {json_response}
"""


JSON_RESPONSE = json.dumps(
    {
        "steps": [
            {
                "type": "'create', 'update', 'overwrite', or 'delete'",
                "path": "Absolute file path",
                "content": "Content to write (required for 'create', 'update', or 'overwrite')",
                "line": "Initial line number where the content should be written (or erased if 'delete')",
            }
        ]
    }
)


def get_prompt(issue_summary: str):
    formatted_input = INPUT.format(issue_summary=issue_summary)
    formatted_output = OUTPUT.format(json_response=JSON_RESPONSE)

    prompt = "\n".join([INSTRUCTION, formatted_input, formatted_output])

    return prompt
