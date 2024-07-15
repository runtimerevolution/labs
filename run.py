import json
import time
from labs.github import GithubRequests
from labs.config import GITHUB_ACCESS_TOKEN, GITHUB_REPO, GITHUB_OWNER, LITELLM_API_KEY
from labs.nlp import NLP_Interface
from labs.context_loading import load_project
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
    prepared_context = []
    for file in context:
        prepared_context.append(
            {"role": "system", "content": f"File: {file['file_name']} Content: {file['content']}"}
        )
    prepared_context.append(
        {
            "role": "user",
            "content": nlp_summary,
        }
    )

    return litellm_requests.completion_without_proxy(prepared_context)


def call_agent_to_apply_code_changes(llm_response, repo_dir):
    response_string = llm_response.choices[0].model_extra["message"].model_extra["content"]
    new_file_name = f"new_issue_{int(time.time())}.py"
    new_file_path = f"{repo_dir}/{new_file_name}"
    new_file = open(new_file_path, "x")
    new_file.write(response_string)
    new_file.close()
    return new_file_path, new_file_name


def commit_changes(branch_name, new_file_path, new_file_name):
    return gh_requests.commit_changes(
        "fix", branch_name=branch_name, files=[{"path": new_file_path, "name": new_file_name}]
    )


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
    change_issue_to_in_progress()
    context, repo_dir = load_context()
    llm_response = call_llm_with_context(
        context, 'Add a file to print sentence "Hello World"'
    )  # nlped_text["summary"])
    new_file_path, new_file_name = call_agent_to_apply_code_changes(llm_response, repo_dir)
    commit_result = commit_changes(branch_name, new_file_path, new_file_name)
    pr_result = create_pull_request(branch_name)
    change_issue_to_in_review()


run()
