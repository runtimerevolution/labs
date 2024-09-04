from labs.github.github import GithubRequests
import labs.fnmatch as fnmatch
import os
from labs.config import GITHUB_ACCESS_TOKEN, GITHUB_OWNER, GITHUB_REPO

# excluded_files= [ 'manage.py', '.*', '*.lock']
excluded_files = [".*"]


def include_file(file_name):
    if file_name in excluded_files:
        return False
    special_files = [string for string in excluded_files if "*" in string]
    for pattern in special_files:
        if fnmatch.fnmatch(file_name, pattern):
            return False
    return True


def collect_project_files(project_path):
    result = []
    for path, subdirs, files in os.walk(project_path):
        for name in files:
            if include_file(name):
                include_dir = True
                dir_names_in_path = path.split("/")[1:]
                for dir_name in dir_names_in_path:
                    if not include_file(dir_name):
                        include_dir = False
                if include_dir:
                    result.append(os.path.join(path, name))
    return result


def get_file_contents(file_names):
    excluded_extensions = [
        ".lock",
        ".backup",
        ".dev",
        ".gz",
        ".br",
        ".jpg",
        ".png",
        ".ico",
        ".dump",
        ".mp4",
        ".pdf",
        ".psd",
        ".webm",
        ".mp3",
        ".gif",
        ".mov",
        ".tif",
        ".bmp",
        ".webp",
        ".enc",
        ".eml",
        ".jpeg",
        "",
        ".pptx",
        ".db",
        ".parquet",
    ]
    file_contents = []
    for file_name in file_names:
        try:
            _, extension = os.path.splitext(file_name)
            if extension not in excluded_extensions:
                with open(file_name, "r") as file:
                    content = file.read()
                    item = {"file_name": file_name, "content": content}
                    file_contents.append(item)
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' was not found.")
        except Exception as e:
            print(f"Error reading file '{file_name}': {e}")

    return file_contents


def load_project():
    ghr = GithubRequests(
        github_token=GITHUB_ACCESS_TOKEN, repo_owner=GITHUB_OWNER, repo_name=GITHUB_REPO
    )
    repo_dir = ghr.clone()
    project_files = collect_project_files(repo_dir)
    files_contents = get_file_contents(project_files)
    return files_contents, repo_dir
