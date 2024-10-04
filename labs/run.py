import logging

from labs.repo import clone_repository
from labs.decorators import time_and_log_function
from labs.middleware import call_llm_with_context, call_agent_to_apply_code_changes
from labs.config import settings
from labs.repo import commit_changes, create_branch, create_pull_request, get_issue


logger = logging.getLogger(__name__)


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
