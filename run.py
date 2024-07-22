import time
from labs.github import GithubRequests
from labs.config import GITHUB_ACCESS_TOKEN, GITHUB_REPO, GITHUB_OWNER, LITELLM_API_KEY
from labs.nlp import NLP_Interface
from labs.context_loading import load_project
from labs.response_parser.parser import create_file, modify_file, parse_llm_output
from litellm_service.request import RequestBarebones  # , RequestLiteLLM

gh_requests: GithubRequests = None
# litellm_requests: RequestLiteLLM = None
barebone_requests: RequestBarebones = None


LLM_PROXY_LITELLM = "LITELLM"
LLM_PROXY_BAREBONES = "BAREBONES"
LLM_PROXY_VALUES = [
    LLM_PROXY_LITELLM,
    LLM_PROXY_BAREBONES,
]
ACTIVE_LLM_PROXY = LLM_PROXY_BAREBONES


def setup():
    global gh_requests
    gh_requests = GithubRequests(
        github_token=GITHUB_ACCESS_TOKEN,
        repo_owner=GITHUB_OWNER,
        repo_name=GITHUB_REPO,
    )

    # global litellm_requests
    # litellm_requests = RequestLiteLLM(LITELLM_API_KEY)
    global barebone_requests
    barebone_requests = RequestBarebones(
        activeloop_dataset_path="hub://cmartinez/labs_db"
    )


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
    if ACTIVE_LLM_PROXY == LLM_PROXY_LITELLM:
        prepared_context = []
        for file in context:
            prepared_context.append(
                {
                    "role": "system",
                    "content": f"File: {file['file_name']} Content: {file['content']}",
                }
            )
        prepared_context.append(
            {
                "role": "user",
                "content": nlp_summary,
            }
        )

        # return litellm_requests.completion_without_proxy(prepared_context)
    elif ACTIVE_LLM_PROXY == LLM_PROXY_BAREBONES:
        return barebone_requests.completion(nlp_summary)


def call_agent_to_apply_code_changes(llm_response, repo_dir):
    response_string = (
        llm_response.choices[0].model_extra["message"].model_extra["content"]
    )
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
    print(nlped_text)
    # change_issue_to_in_progress()
    context, repo_dir = load_context()
    nlp_summary = f"""
    Add a multiplication function to the Calculator class in labs/code_examples/calculator.py and add a unit tests for the new multiplication function in the file labs/code_examples/test_calculator.py file.
    """
    llm_response = call_llm_with_context(context, nlp_summary)  # nlped_text["summary"])
    new_file_path, new_file_name = call_agent_to_apply_code_changes(
        llm_response, repo_dir
    )
    commit_result = commit_changes(branch_name, new_file_path, new_file_name)
    pr_result = create_pull_request(branch_name)
    # change_issue_to_in_review()


run()
