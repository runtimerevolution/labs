from dataclasses import dataclass
import logging

from litellm_service.request import PullRequest

logger = logging.getLogger(__name__)


@dataclass
class Action:
    step_number: int
    action_type: str
    path: str
    content: str


def clean_yaml_string(yaml_string):
    # Remove the ```yaml at the beginning and ``` at the end if they exist
    if yaml_string.startswith("```yaml"):
        yaml_string = yaml_string[len("```yaml") :].strip()
    if yaml_string.endswith("```"):
        yaml_string = yaml_string[: -len("```")].strip()

    return yaml_string


def parse_llm_output(text_output):
    return PullRequest.model_validate_json(text_output)


def create_file(path, content):
    logger.debug(f"Creating file on path: {path}")
    try:
        with open(path, "w") as file:
            file.write(content)
        logger.debug(f"File created at {path}")
        return path
    except Exception as e:
        logger.error(f"Error creating file at {path}: {e}")
        return None


def modify_file(path, content):
    logger.debug(f"Creating file on path: {path}")
    try:
        with open(path, "w") as file:
            file.write("\n" + content)
        logger.debug(f"File modified at {path}")
        return path
    except Exception as e:
        logger.error(f"Error modifying file at {path}: {e}")
        return None
