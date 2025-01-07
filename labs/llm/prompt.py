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
    - 'create': Creates a new file with the specified content.  
    - 'update': Appends the content at the given line of an existing file.  
    - 'overwrite': Replaces content at the specified line in the file.  
    - 'delete': Removes content from the specified line in the file.
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
