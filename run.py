from labs.api.types import CodeMonkeyRequest, GithubModel
from labs.decorators import time_and_log_function
from labs.github.github import GithubRequests
import logging
from labs.middleware import call_llm_with_context, call_agent_to_apply_code_changes


logger = logging.getLogger(__name__)

gh_requests: GithubRequests = None


@time_and_log_function
def setup(request: CodeMonkeyRequest):
    global gh_requests
    gh_requests = GithubRequests(
        github_token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
    )


@time_and_log_function
def get_issue(issue_number):
    return gh_requests.get_issue(issue_number)


@time_and_log_function
def create_branch(issue_number, issue_title):
    branch_name = f"{issue_number}-{issue_title}"
    create_result = gh_requests.create_branch(branch_name=branch_name)
    return create_result, branch_name


@time_and_log_function
def change_issue_to_in_progress():
    pass


@time_and_log_function
def commit_changes(branch_name, file_list):
    return gh_requests.commit_changes("fix", branch_name=branch_name, files=file_list)


@time_and_log_function
def create_pull_request(branch_name, title):
    return gh_requests.create_pull_request(branch_name, title=title)


@time_and_log_function
def change_issue_to_in_review():
    pass


@time_and_log_function
def run(request: CodeMonkeyRequest):
    setup(request)
    issue = get_issue(request.issue_number)
    _, branch_name = create_branch(
        request.issue_number, issue["title"].replace(" ", "-")
    )

    github = GithubModel(
        github_token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
    )
    success, llm_response = call_llm_with_context(
        github=github,
        issue_summary=issue["body"],
        litellm_api_key=request.litellm_api_key,
    )
    if not success:
        logger.error("Failed to get a response from LLM, aborting run.")
        return

    response_output = call_agent_to_apply_code_changes(llm_response)

    commit_changes(branch_name, response_output)
    create_pull_request(branch_name, issue["title"])
