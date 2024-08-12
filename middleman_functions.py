from labs.api.types import GithubModel
from labs.response_parser.parser import create_file, modify_file, parse_llm_output
from litellm_service.request import RequestLiteLLM
from rag.rag import find_similar_embeddings
from vector.vectorize_to_db import vectorize_to_db
from labs.config import CLONE_DESTINATION_DIR, LLM_MODEL_NAME, get_logger

logger = get_logger(__name__)

def call_llm_with_context(github: GithubModel, issue_summary, litellm_api_key):
    if not issue_summary:
        raise ValueError("issue_summary cannot be empty")
    litellm_requests = RequestLiteLLM(litellm_api_key)
    destination = CLONE_DESTINATION_DIR + f"{github.repo_owner}/{github.repo_name}"
    vectorize_to_db(f"https://github.com/{github.repo_owner}/{github.repo_name}", None, destination)
    # find_similar_embeddings narrows down codebase to files that matter for the issue at hand.
    context = find_similar_embeddings(issue_summary)
    prompt = f"""
    You're a diligent software engineer AI. You can't see, draw, or interact with a 
    browser, but you can read and write files, and you can think.
    You've been given the following task: {issue_summary}. Your answer will be in yaml format.
    Please provide a list of actions to perform in order to complete it, considering the current project, cloned into {destination} .
    Any imports will be at the beggining of the file.
    Add tests for the new functionalities, considering any existing test files.
    Each action should contain two fields:
    action, which is either 'create' to add a new file  or 'modify' to edit an existing one;
    args, which is a map of key-value pairs, specifying the arguments for that action:
    path - the absolute path of the file to create/modify and content - the content to write to the file.
    If the file is to be modify, on the contents send the finished version of the entire file.
    Please don't add any text formatting to the answer, making it as clean as possible.
    
    **Output example**:
    
    - action: create
      args:
          path: path_to_some_file
          content: |
          some file content
  
    - action: modify
      args:
          path: path_to_some_other_file
          content: |
          some other file content
    """
    prepared_context = []
    for file in context:
        prepared_context.append(
            {
                "role": "system",
                "content": f"File: {file[1]} Content: {file[2]}",
            }
        )
    prepared_context.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    try:
        llm_response = litellm_requests.completion_without_proxy(
            prepared_context,
            model=LLM_MODEL_NAME,
        )

    except Exception as e:
        logger.error(f"Error calling LLM: {str(e)}")

    output = call_agent_to_apply_code_changes(llm_response)
    return output


def call_agent_to_apply_code_changes(llm_response):
    response_string = llm_response[1].choices[0].message.content
    # Find actions to apply from the llm_response
    actions = parse_llm_output(response_string)
    files = []
    # Apply the actions
    for action in actions:
        if action.action_type == "create":
            files.append(create_file(action.path, action.content))
        elif action.action_type == "modify":
            files.append(modify_file(action.path, action.content))
        else:
            print(f"Unknown action '{action.action_type}' in step {action.step_number}")

    return files
