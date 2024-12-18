import json

JSON_RESPONSE = json.dumps(
    {
        "steps": [
            {
                "type": "String field, either 'create', 'modify' or 'overwrite'",
                "path": "String field, the absolute path of the file to create/modify",
                "content": "String field, the content to write to the file",
                "line": "Integer optional field, should only be included if the type is 'modify'. This field should be the number of the first line where the content should be written.",
            },
        ]
    }
)


def get_prompt(issue_summary: str):
    return f"""
    You are an advanced Python coding assistant designed to resolve issues for Python-based repositories. 
    You will receive:
    1. A description of the issue.
    2. File names and their contents as context (already provided in the system message).
    3. Constraints such as not modifying migrations unless explicitly required.
    
    Your task is to:
    - Analyze the provided issue description and associated context.
    - Generate the necessary Python code changes to resolve the issue.
    - Ensure adherence to Python best practices.
    - Avoid changes to migrations or unrelated files unless specified.
    - Provide clean, commented, and ready-to-review code changes.
    
    Issue Description:
    {issue_summary}

    Your Task:
    Based on the issue description and the provided system context, write the Python code changes 
    required to resolve the issue. 
    - Show only the updated or added code with inline comments explaining the changes.
    - Do not modify database migrations unless explicitly requested.
    - Ensure the changes are consistent with the rest of the project.
    
    You must provide a JSON response in the following format: {JSON_RESPONSE}
    """
