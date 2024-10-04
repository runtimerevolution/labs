import logging

from labs.decorators import time_and_log_function
from labs.github.github import GithubRequests


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
