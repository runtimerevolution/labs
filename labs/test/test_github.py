import pytest
import vcr
from labs.github import GithubRequests
from labs.config import GITHUB_ACCESS_TOKEN

@pytest.fixture
def github_instance():
    return GithubRequests()

@vcr.use_cassette('labs/test/vcr_cassettes/github_issue_invalid_token.yml')
def test_issue_invalid_token(github_instance):
    github_instance.access_token = 'invalid_token'
    issue_id = 1
    issue = github_instance.issue(issue_id)
    assert issue is None
        
@vcr.use_cassette('labs/test/vcr_cassettes/github_issues_invalid_token.yml')
def test_issues_invalid_token(github_instance):
    github_instance.access_token = 'invalid_token'
    issues = github_instance.issues()
    assert issues == []

@vcr.use_cassette('labs/test/vcr_cassettes/issues.yaml')
def test_issues(github_instance):
    issues = github_instance.issues()
    assert isinstance(issues, list)
    if issues:
        assert 'title' in issues[0]

@vcr.use_cassette('labs/test/vcr_cassettes/issue.yaml')
def test_issue(github_instance):
    issue_id = 1  # Replace with an actual issue ID that you expect to exist
    issue = github_instance.issue(issue_id)
    assert isinstance(issue, dict)
    assert 'title' in issue
      
@vcr.use_cassette('labs/test/vcr_cassettes/issues_from_all_assignees.yaml')
def test_issues_with_assignee(github_instance):
    issues = github_instance.issues(assignee='all')
    assert isinstance(issues, list)
    if issues:
        assert 'title' in issues[0]

@vcr.use_cassette('labs/test/vcr_cassettes/issues_with_state.yaml')
def test_issues_with_state(github_instance):
    issues = github_instance.issues(state='closed')
    assert isinstance(issues, list)
    if issues:
        assert issues[0]['state'] == 'closed'

@vcr.use_cassette('labs/test/vcr_cassettes/issue_not_found.yaml')
def test_issue_not_found(github_instance):
    issue_id = 999999  # Non-existent issue ID
    issue = github_instance.issue(issue_id)
    assert issue is None

