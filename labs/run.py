import logging

import config.configuration_variables as settings
from decorators import time_and_log_function
from llm import call_llm_with_context
from repo import (
    call_agent_to_apply_code_changes,
    clone_repository,
    commit_changes,
    create_branch,
    create_pull_request,
    get_issue,
)

logger = logging.getLogger(__name__)


@time_and_log_function
def run_on_repository(token, repository_owner, repository_name, username, issue_number, original_branch="main"):
    issue = get_issue(token, repository_owner, repository_name, username, issue_number)
    issue_title = issue["title"].replace(" ", "-")
    issue_summary = issue["body"]

    branch_name = create_branch(
        token,
        repository_owner,
        repository_name,
        username,
        issue_number,
        issue_title,
        original_branch,
    )

    repository_url = f"https://github.com/{repository_owner}/{repository_name}"
    logger.debug(f"Cloning repository from {repository_url}")

    repository_path = f"{settings.CLONE_DESTINATION_DIR}{repository_owner}/{repository_name}"
    clone_repository(repository_url, repository_path)

    success, llm_response = call_llm_with_context(repository_path, issue_summary)
    if not success:
        logger.error("Failed to get a response from LLM, aborting run.")
        return

    response_output = call_agent_to_apply_code_changes(llm_response[1].choices[0].message.content)

    commit_changes(token, repository_owner, repository_name, username, branch_name, response_output)
    create_pull_request(token, repository_owner, repository_name, username, branch_name)


@time_and_log_function
def run_on_local_repo(repository_path, issue_text):
    success, llm_response = call_llm_with_context(repository_path, issue_text)
    if not success:
        logger.error("Failed to get a response from LLM, aborting run.")
        return

    response_output = call_agent_to_apply_code_changes(llm_response[1].choices[0].message.content)
    return True, response_output
