import logging

from labs.database.vectorize_to_db import clone_repository
from labs.decorators import time_and_log_function
from labs.github.github import GithubRequests
from labs.middleware import call_llm_with_context, call_agent_to_apply_code_changes
from labs.config import settings


logger = logging.getLogger(__name__)


@time_and_log_function
def get_issue(token, repo_owner, repo_name, username, issue_number):
    github_request = GithubRequests(github_token=token, repo_owner=repo_owner, repo_name=repo_name, username=username)
    return github_request.get_issue(issue_number)


@time_and_log_function
def create_branch(token, repo_owner, repo_name, username, issue_number, issue_title, original_branch="main"):
    github_request = GithubRequests(github_token=token, repo_owner=repo_owner, repo_name=repo_name, username=username)
    branch_name = f"{issue_number}-{issue_title}"
    github_request.create_branch(branch_name=branch_name, original_branch=original_branch)
    return branch_name


@time_and_log_function
def change_issue_to_in_progress():
    pass


@time_and_log_function
def commit_changes(token, repo_owner, repo_name, username, branch_name, file_list):
    github_request = GithubRequests(github_token=token, repo_owner=repo_owner, repo_name=repo_name, username=username)
    return github_request.commit_changes("fix", branch_name=branch_name, files=file_list)


@time_and_log_function
def create_pull_request(token, repo_owner, repo_name, username, original_branch, branch_name):
    github_request = GithubRequests(github_token=token, repo_owner=repo_owner, repo_name=repo_name, username=username)
    return github_request.create_pull_request(branch_name, base=original_branch)


@time_and_log_function
def change_issue_to_in_review():
    pass


@time_and_log_function
def run_on_repo(token, repo_owner, repo_name, username, issue_number, original_branch="main"):
    issue = get_issue(token, repo_owner, repo_name, username, issue_number)
    issue_title = issue["title"].replace(" ", "-")
    issue_summary = issue["body"]

    branch_name = create_branch(token, repo_owner, repo_name, username, issue_number, issue_title, original_branch)

    repo_url = f"https://github.com/{repo_owner}/{repo_name}"
    logger.debug(f"Cloning repo from {repo_url}")

    repo_destination = settings.CLONE_DESTINATION_DIR + f"{repo_owner}/{repo_name}"
    clone_repository(repo_url, repo_destination)

    success, llm_response = call_llm_with_context(repo_destination, issue_summary)
    if not success:
        logger.error("Failed to get a response from LLM, aborting run.")
        return

    response_output = call_agent_to_apply_code_changes(llm_response[1].choices[0].message.content)

    commit_changes(token, repo_owner, repo_name, username, branch_name, response_output)
    create_pull_request(token, repo_owner, repo_name, username, branch_name)


@time_and_log_function
def run_on_local_repo(repo_path, issue_text):
    success, llm_response = call_llm_with_context(repo_path, issue_text)
    if not success:
        logger.error("Failed to get a response from LLM, aborting run.")
        return

    response_output = call_agent_to_apply_code_changes(llm_response[1].choices[0].message.content)
    return True, response_output
