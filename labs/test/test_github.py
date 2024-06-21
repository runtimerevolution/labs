import vcr
import pytest
from labs.github import get_issue, get_issues_from_repo
from labs.config import GITHUB_ACCESS_TOKEN

# Tests for get_issue
@vcr.use_cassette('labs/test/fixtures/vcr_cassettes/github_issue_invalid_token.yml')
def test_get_issue_invalid_token():
    global GITHUB_ACCESS_TOKEN
    original_token = GITHUB_ACCESS_TOKEN
    try:
        GITHUB_ACCESS_TOKEN = 'invalid_token'
        issue_id = 1
        issue = get_issue.get_issue(issue_id)
        assert issue is None
    finally:
        GITHUB_ACCESS_TOKEN = original_token

@vcr.use_cassette('labs/test/fixtures/vcr_cassettes/github_issue.yml')
def test_get_issue_success():
    issue_id = 1
    issue = get_issue.get_issue(issue_id)
    assert issue is not None
    assert 'title' in issue
    assert 'body' in issue

@vcr.use_cassette('labs/test/fixtures/vcr_cassettes/github_issue_not_found.yml')
def test_get_issue_not_found():
    issue_id = 99999
    issue = get_issue.get_issue(issue_id)
    assert issue is None

# Tests for get_issues_from_repo
@vcr.use_cassette('labs/test/fixtures/vcr_cassettes/github_issues_invalid_token.yml')
def test_get_issues_from_repo_invalid_token():
    global GITHUB_ACCESS_TOKEN
    original_token = GITHUB_ACCESS_TOKEN
    try:
        GITHUB_ACCESS_TOKEN = 'invalid_token'
        issues = get_issues_from_repo.get_issues_from_repo()
        assert issues == []
    finally:
        GITHUB_ACCESS_TOKEN = original_token

@vcr.use_cassette('labs/test/fixtures/vcr_cassettes/github_issues.yml')
def test_get_issues_from_repo_success():
    issues = get_issues_from_repo.get_issues_from_repo()
    assert isinstance(issues, list)
    if issues:
        assert 'title' in issues[0]
        assert 'state' in issues[0]

@vcr.use_cassette('labs/test/fixtures/vcr_cassettes/github_issues_no_assignee.yml')
def test_get_issues_from_repo_no_assignee():
    issues = get_issues_from_repo.get_issues_from_repo(assignee='all')
    assert isinstance(issues, list)
    if issues:
        assert 'title' in issues[0]
        assert 'state' in issues[0]

@vcr.use_cassette('labs/test/fixtures/vcr_cassettes/github_issues_closed.yml')
def test_get_issues_from_repo_closed_issues():
    issues = get_issues_from_repo.get_issues_from_repo(state='closed')
    assert isinstance(issues, list)
    if issues:
        assert 'title' in issues[0]
        assert 'state' in issues[0]
        assert issues[0]['state'] == 'closed'


