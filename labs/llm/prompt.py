import json

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
    return f"""
    You are an advanced Python coding assistant designed to resolve tasks for Python-based code. 
    You will receive:
        1. A description of the task.
        2. File names and their contents as context (already provided in the system message).
        3. Constraints such as not modifying migrations unless explicitly required.

    You should:
        - Analyze the provided task description and associated context.
        - Generate the necessary Python code changes to resolve the task.
        - Ensure adherence to Python best practices.
        - Avoid changes to migrations or unrelated files unless specified.
        - Provide clean, organized, and ready-to-review code changes.
        - Group related logic together to ensure clarity and cohesion.
        - Add meaningful comments to explain non-obvious logic or complex operations.
        - Ensure the code integrates seamlessly into the existing structure of the project.

    Task description:
        {issue_summary}
    
    Based on the task description and the provided system context:
        - Write the Python code changes required to resolve the task.
        - Ensure that changes are made only within the allowed scope.
    
    You must provide a JSON response in the following format: {JSON_RESPONSE}
    
    Perform the 'delete' operations in reverse line number order to avoid line shifting.
    """
