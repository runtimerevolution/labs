from labs.github.get_issues_from_repo import get_issues_from_repo
from labs.github.get_issue import get_issue
from labs.github.get_issue import issue_body

def main():
    # print(get_issues_from_repo())
    # print()
    # print(get_issue(1))
    print(issue_body(get_issue(1)))

if __name__ == "__main__":
    main()