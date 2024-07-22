from dataclasses import dataclass
import yaml


@dataclass
class Action:
    step_number: int
    action_type: str
    path: str
    content: str


def parse_llm_output(text_output):
    # Load the YAML text
    data = yaml.safe_load(text_output)

    # Create a list to store the steps
    steps = []

    # Extract and store the information in Step objects
    for i, item in enumerate(data, start=1):
        action = item.get("action")
        path = item.get("args", {}).get("path")
        content = item.get("args", {}).get("content")
        steps.append(Action(step_number=i, action_type=action, path=path, content=content.strip()))

    return steps


def create_file(path, content):
    try:
        with open(path, "w") as file:
            file.write(content)
        print(f"File created at {path}")
        return path
    except Exception as e:
        print(f"Error creating file at {path}: {e}")
        return None


def modify_file(path, content):
    try:
        with open(path, "a") as file:
            file.write("\n" + content)
        print(f"File modified at {path}")
        return path
    except Exception as e:
        print(f"Error modifying file at {path}: {e}")
        return None