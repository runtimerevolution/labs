from labs.context_loading import load_project
from labs.github import GithubRequests
from labs.config import GITHUB_ACCESS_TOKEN, GITHUB_REPO, GITHUB_OWNER, LITELLM_API_KEY
from labs.nlp import NLP_Interface
from labs.response_parser.parser import create_file, modify_file, parse_llm_output
from litellm_service.request import RequestLiteLLM
from pgvector.vectorize_to_db import vectorize_to_db
from pgvector.queries import select_embeddings

gh_requests: GithubRequests = None
litellm_requests: RequestLiteLLM = None


def setup():
    global gh_requests
    gh_requests = GithubRequests(
        github_token=GITHUB_ACCESS_TOKEN,
        repo_owner=GITHUB_OWNER,
        repo_name=GITHUB_REPO,
    )

    global litellm_requests
    litellm_requests = RequestLiteLLM(LITELLM_API_KEY)


def get_issue(issue_number):
    return gh_requests.get_issue(issue_number)


def create_branch(issue_number, issue_title):
    branch_name = f"{issue_number}-{issue_title}"
    create_result = gh_requests.create_branch(branch_name=branch_name)
    return create_result, branch_name


def apply_nlp_to_issue(issue_text):
    nlp = NLP_Interface(issue_text)
    return nlp.run()


def change_issue_to_in_progress():
    pass


def load_context():
    destination = f"/tmp/{GITHUB_OWNER}/{GITHUB_REPO}"
    vectorize_to_db("https://github.com/runtimerevolution/labs", None, destination)
    return select_embeddings(), destination


def call_llm_with_context(context, nlp_summary):
    prepared_context = []
    for file in context:
        if (
            file[2] == "/tmp/runtimerevolution/labs/code_examples/__init__.py"
            or file[2] == "/tmp/runtimerevolution/labs/code_examples/calculator.py"
            or file[2] == "/tmp/runtimerevolution/labs/code_examples/test_calculator.py"
        ):
            prepared_context.append(
                {
                    "role": "system",
                    "content": f"File: {file[2]} Content: {file[3]}",
                }
            )
    prepared_context.append(
        {
            "role": "user",
            "content": nlp_summary,
        }
    )

    return litellm_requests.completion_without_proxy(
        prepared_context,
        model="openai/gpt-3.5-turbo",
    )


def call_agent_to_apply_code_changes(llm_response, repo_dir):
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


def commit_changes(branch_name, file_list):
    return gh_requests.commit_changes("fix", branch_name=branch_name, files=file_list)


def create_pull_request(branch_name):
    return gh_requests.create_pull_request(branch_name)


def change_issue_to_in_review():
    pass


def run():
    issue_number = 35

    setup()
    issue = get_issue(issue_number)
    branch, branch_name = create_branch(issue_number, issue["title"].replace(" ", "-"))
    nlped_text = apply_nlp_to_issue(issue["body"])
    # change_issue_to_in_progress()
    context, repo_dir = load_context()
    nlp_summary = f"""
    Add a multiplication function to the Calculator class in labs/code_examples/calculator.py and add a unit tests for the new multiplication function in the file labs/code_examples/test_calculator.py file.
    """
    user_input = f"""
    You're a diligent software engineer AI. You can't see, draw, or interact with a browser, but you can read and write files, and you can think.
    You've been given the following task: {nlp_summary}. Your answer will be in yaml format. Please provide a list of actions to perform in order to complete it, considering the current project.
    Each action should contain two fields: action, which is either create or modify; and args, which is a map of key-value pairs, specifying the arguments for that action:
    path - the path of the file to create/modify and content - the content to write to the file.
    Please don't add any text formatting to the answer, making it as clean as possible.
    """
    llm_response = call_llm_with_context(context, user_input)  # nlped_text["summary"])
    new_file_path, new_file_name = call_agent_to_apply_code_changes(
        llm_response, repo_dir
    )
    commit_result = commit_changes(branch_name, new_file_path, new_file_name)
    pr_result = create_pull_request(branch_name)
    # change_issue_to_in_review()
