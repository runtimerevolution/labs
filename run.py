from labs.api.types import CodeMonkeyRequest, GithubModel
from labs.config.settings import (
    GITHUB_ACCESS_TOKEN,
    GITHUB_REPO,
    GITHUB_OWNER,
)
from labs.github.github import GithubRequests
from labs.middleware import call_llm_with_context


gh_requests: GithubRequests = None


def setup():
    global gh_requests
    gh_requests = GithubRequests(
        github_token=GITHUB_ACCESS_TOKEN,
        repo_owner=GITHUB_OWNER,
        repo_name=GITHUB_REPO,
    )


def get_issue(issue_number):
    return gh_requests.get_issue(issue_number)


def create_branch(issue_number, issue_title):
    branch_name = f"{issue_number}-{issue_title}"
    create_result = gh_requests.create_branch(branch_name=branch_name)
    return create_result, branch_name


def change_issue_to_in_progress():
    pass


def commit_changes(branch_name, file_list):
    return gh_requests.commit_changes("fix", branch_name=branch_name, files=file_list)


def create_pull_request(branch_name):
    return gh_requests.create_pull_request(branch_name)


def change_issue_to_in_review():
    pass


def run(request: CodeMonkeyRequest):
    setup()
    issue = get_issue(request.issue_number)
    _, branch_name = create_branch(
        request.issue_number, issue["title"].replace(" ", "-")
    )

    github = GithubModel(
        github_token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
    )
    response_output = call_llm_with_context(
        github=github,
        issue_summary=issue["body"],
        litellm_api_key=request.litellm_api_key,
    )
    commit_changes(branch_name, response_output)
    create_pull_request(branch_name)
