import time
from labs.github import GithubRequests
from labs.config import GITHUB_ACCESS_TOKEN, GITHUB_REPO, GITHUB_OWNER, LITELLM_API_KEY
from labs.nlp import NLP_Interface
from labs.context_loading import load_project
from labs.response_parser.parser import create_file, modify_file, parse_llm_output
from litellm_service.request import RequestLiteLLM

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
    return load_project()


def call_llm_with_context(context, nlp_summary):
    prompt = f"""
    You're a diligent software engineer AI. You can't see, draw, or interact with a 
    browser, but you can read and write files, and you can think.
    You've been given the following task: {nlp_summary}.Your answer will be in yaml format. Please provide a list of actions to perform in order to complete it, considering the current project.
    Each action should contain two fields: action, which is either create or modify,and args, which is a map of key-value pairs, specifying the arguments for that action:
    path - the path of the file to create/modify and content - the content to write to the file.
    Please don't add any text formatting to the answer, making it as clean as possible.
    """

    prepared_context = []
    for file in context:
        prepared_context.append(
            {"role": "system", "content": f"File: {file['file_name']} Content: {file['content']}"}
        )
    prepared_context.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    return litellm_requests.completion_without_proxy(prepared_context)


def call_agent_to_apply_code_changes(llm_response, repo_dir):
    response_string = llm_response.choices[0].model_extra["message"].model_extra["content"]
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
    llm_response = call_llm_with_context(
        context,
        'Add a file to print sentence "Hello World", add a file with a method do calculate the sum of two numbers',
    )  # nlped_text["summary"])
    files = call_agent_to_apply_code_changes(llm_response, repo_dir)
    commit_result = commit_changes(branch_name, file_list=files)
    pr_result = create_pull_request(branch_name)
    # change_issue_to_in_review()


run()
