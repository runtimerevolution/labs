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
    return f"""
        You're a diligent software engineer AI. You can't see, draw, or interact with a 
        browser, but you can read and write files, and you can think.
        You've been given the following task: {issue_summary}.
        Any imports will be at the beggining of the file.
        Add tests for the new functionalities, considering any existing test files.
        The file paths provided are **absolute paths relative to the project root**, 
        and **must not be changed**. Ensure the paths you output match the paths provided exactly. 
        Do not prepend or modify the paths.
        Please provide a json response in the following format: {JSON_RESPONSE}
    """
