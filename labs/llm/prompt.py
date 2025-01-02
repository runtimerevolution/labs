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


JSON_RESPONSE = {
    "steps": [
        {
            "type": "String field, either 'create' or 'modify'",
            "path": "String field, the absolute path of the file to create/modify",
            "content": "String field, the content to write to the file",
            "line": "Integer optional field, should only be included if the type is 'modify'. This field should be the number of the first line where the content should be written.",
        },
    ]
}


def get_prompt(issue_summary: str):
    input = INPUT.format(issue_summary=issue_summary)
    output = OUTPUT.format(json_response=JSON_RESPONSE)

    prompt = "\n".join([INSTRUCTION, input, output])

    return prompt
