import pytest
import vcr
from labs.github import Github
from labs.config import GITHUB_ACCESS_TOKEN

@pytest.fixture
def github_instance():
    return Github()

@vcr.use_cassette('labs/test/vcr_cassettes/github_issue_invalid_token.yml')
def test_get_issue_invalid_token(github_instance):
    github_instance.access_token = 'invalid_token'
    issue_id = 1
    issue = github_instance.get_issue(issue_id)
    assert issue is None
        
@vcr.use_cassette('labs/test/vcr_cassettes/github_issues_invalid_token.yml')
def test_get_issues_from_repo_invalid_token(github_instance):
    github_instance.access_token = 'invalid_token'
    issues = github_instance.get_issues_from_repo()
    assert issues == []

@vcr.use_cassette('labs/test/vcr_cassettes/get_issues_from_repo.yaml')
def test_get_issues_from_repo(github_instance):
    issues = github_instance.get_issues_from_repo()
    assert isinstance(issues, list)
    if issues:
        assert 'title' in issues[0]

@vcr.use_cassette('labs/test/vcr_cassettes/get_issue.yaml')
def test_get_issue(github_instance):
    issue_id = 1  # Replace with an actual issue ID that you expect to exist
    issue = github_instance.get_issue(issue_id)
    assert isinstance(issue, dict)
    assert 'title' in issue

@vcr.use_cassette('labs/test/vcr_cassettes/issue_body.yaml')
def test_issue_body(github_instance):
    issue_id = 1  # Replace with an actual issue ID that you expect to exist
    issue = github_instance.get_issue(issue_id)
    if issue:
        body = github_instance.issue_body(issue)
        assert isinstance(body, str)
    else:
        pytest.skip("No issue found to test issue_body")
      
@vcr.use_cassette('labs/test/vcr_cassettes/get_issues_from_repo_from_all_assignees.yaml')
def test_get_issues_from_repo_with_assignee(github_instance):
    issues = github_instance.get_issues_from_repo(assignee='all')
    assert isinstance(issues, list)
    if issues:
        assert 'title' in issues[0]

@vcr.use_cassette('labs/test/vcr_cassettes/get_issues_from_repo_with_state.yaml')
def test_get_issues_from_repo_with_state(github_instance):
    issues = github_instance.get_issues_from_repo(state='closed')
    assert isinstance(issues, list)
    if issues:
        assert issues[0]['state'] == 'closed'

@vcr.use_cassette('labs/test/vcr_cassettes/get_issue_not_found.yaml')
def test_get_issue_not_found(github_instance):
    issue_id = 999999  # Non-existent issue ID
    issue = github_instance.get_issue(issue_id)
    assert issue is None

@vcr.use_cassette('labs/test/vcr_cassettes/issue_body_no_body.yaml')
def test_issue_body_no_body(github_instance):
    issue_id = 1  # Existing issue ID
    issue = github_instance.get_issue(issue_id)
    if issue:
        issue.pop('body', None)
        body = github_instance.issue_body(issue)
        assert body is None
    else:
        pytest.skip("No issue found to test issue_body_no_body")
