# snippet:
# title: "GitHub Default Branch from a Repo URL"
# card_title: "GitHub Default Branch"
# summary: "Parse a GitHub repository URL and return its default branch name from the GitHub API."
# tags: [github, git]
# added: "2026-09-30T17:33:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs the requests package. GitHub HTTPS URLs only, in owner/repo form. Unauthenticated API calls are rate-limited."
# end-snippet
from urllib.parse import urlparse

import requests


def get_default_branch(repo_url: str) -> str:
    """Return the default branch for a GitHub repository URL."""

    path = urlparse(repo_url).path.removesuffix(".git").strip("/")
    owner, repo = path.split("/")

    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}",
        timeout=10,
    )
    response.raise_for_status()

    return response.json()["default_branch"]


repo_url = "https://github.com/owner/repository"
print(get_default_branch(repo_url))
