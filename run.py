import logging

from labs.api.types import GithubModel, RunRequest
from labs.decorators import time_and_log_function
from labs.github.github import GithubRequests
from labs.middleware import call_llm_with_context, call_agent_to_apply_code_changes


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
def change_issue_to_in_progress(self):
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
def change_issue_to_in_review(self):
    pass


class Run:
    def __init__(self, request: RunRequest):
        self.request = request
        self.github_request = GithubRequests(
            github_token=request.github_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            username=request.username,
        )

    @time_and_log_function
    def get_issue(self):
        return self.github_request.get_issue(self.request.issue_number)

    @time_and_log_function
    def create_branch(self, issue_title):
        branch_name = f"{self.request.issue_number}-{issue_title}"
        self.github_request.create_branch(branch_name=branch_name, original_branch=self.request.original_branch)
        return branch_name

    @time_and_log_function
    def change_issue_to_in_progress(self):
        pass

    @time_and_log_function
    def commit_changes(self, branch_name, file_list):
        return self.github_request.commit_changes("fix", branch_name=branch_name, files=file_list)

    @time_and_log_function
    def create_pull_request(self, branch_name):
        return self.github_request.create_pull_request(branch_name, base=self.request.original_branch)

    @time_and_log_function
    def change_issue_to_in_review(self):
        pass

    @time_and_log_function
    def run(self):
        issue = self.get_issue()
        branch_name = self.create_branch(issue["title"].replace(" ", "-"))

        github = GithubModel(
            token=self.request.github_token,
            repo_owner=self.request.repo_owner,
            repo_name=self.request.repo_name,
        )
        success, llm_response = call_llm_with_context(github=github, issue_summary=issue["body"])
        if not success:
            logger.error("Failed to get a response from LLM, aborting run.")
            return

        response_output = call_agent_to_apply_code_changes(llm_response[1].choices[0].message.content)

        self.commit_changes(branch_name, response_output)
        self.create_pull_request(branch_name)
