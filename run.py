import json
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
    return gh_requests.create_branch(branch_name=f"{issue_number}/{issue_title}")


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
            {"role": "system", "context": f"File: {file['file_name']} Content: {file['content']}"}
        )
    prepared_context.append(
        {
            "role": "user",
            "context": nlp_summary,
        }
    )

    return litellm_requests.completion(prepared_context)


def call_agent_to_apply_code_changes(llm_response):
    return None


def commit_changes(id):
    return None


def create_pull_request(id):
    return None


def change_issue_to_in_review(id):
    return None


def run():
    issue_number = 35

    setup()
    issue = get_issue(issue_number)
    branch = create_branch(issue_number, issue["title"])
    nlped_text = apply_nlp_to_issue(issue["body"])
    change_issue_to_in_progress()
    context = load_context()
    llm_response = call_llm_with_context(context, 'Add a file to print sentence "Hello World"')
    call_agent_to_apply_code_changes(llm_response)
    commit_changes()
    create_pull_request()
    change_issue_to_in_review(id)


run()
