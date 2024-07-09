from labs.github import GithubRequests
import labs.fnmatch as fnmatch
import os

#excluded_files= [ 'manage.py', '.*', '*.lock']
excluded_files= [ '.*' ]

def include_file(file_name):
    if file_name in excluded_files:
        return False
    special_files = [string for string in excluded_files if '*' in string]
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
                dir_names_in_path = path.split('/')[1:]
                for dir_name in dir_names_in_path:
                    if not include_file(dir_name):
                        include_dir = False
                if include_dir:
                    result.append(os.path.join(path, name))
    return result


def load_project():
    ghr = GithubRequests()
    repo_dir = ghr.clone()
    project_files = collect_project_files(repo_dir)
    return project_files
    
    

