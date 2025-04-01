import os
from github import Github
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN not set in environment variables!")

g = Github(token)
REPO_OWNER = "crystal-lang"
REPO_NAME = "crystal"
LANGUAGE = "crystal"


repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

def count_repositories_by_language(language):
    query = f"language:{language}"
    repos = g.search_repositories(query)
    return repos.totalCount


def get_stars(repo):
    return repo.stargazers_count


def get_forks(repo):
    return repo.forks_count


def get_commit_count(repo):
    branch = repo.get_branch(repo.default_branch)
    return repo.get_commits(sha=branch.commit.sha).totalCount


def get_open_prs(repo):
    prs = repo.get_pulls(state="open")
    return prs.totalCount


def get_avg_pr_close_time(repo):
    prs = repo.get_pulls(state="closed", sort="created", direction="desc")
    total_time = 0
    count = 0

    for pr in prs:
        if pr.closed_at and pr.created_at:
            total_time += (pr.closed_at - pr.created_at).total_seconds()
            count += 1

    if count == 0:
        return 0
    return total_time / count / 3600

print(f"Number of {LANGUAGE} repositories: {count_repositories_by_language(LANGUAGE)}")
print(f"Stars: {get_stars(repo)}")
print(f"Forks: {get_forks(repo)}")
print(f"Commits: {get_commit_count(repo)}")
print(f"Open PRs: {get_open_prs(repo)}")
print(f"Average PR close time (hours): {get_avg_pr_close_time(repo):.2f}")