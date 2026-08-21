# snippet:
# title: "Switch a GitHub SSH remote to HTTPS"
# card_title: "SSH remote to HTTPS"
# summary: "Rewrite a GitHub git@ or ssh:// remote to https://github.com/owner/repo.git after checking the current directory is a git work tree."
# tags: [git]
# added: "2026-08-21T12:53:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "GitHub remotes only. Call github_ssh_to_https or github_ssh_to_https origin. Leaves the URL unchanged if it is already HTTPS."
# end-snippet
github_ssh_to_https() {
  local remote=${1:-origin}
  local url owner repo new_url

  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Not a git repository." >&2
    return 1
  fi

  if ! url=$(git remote get-url "$remote" 2>/dev/null); then
    echo "Remote ${remote} is not configured." >&2
    return 1
  fi

  if [[ $url == https://github.com/* ]]; then
    echo "${remote} is already HTTPS: ${url}"
    return 0
  fi

  if [[ $url =~ ^git@github\.com:([^/]+)/([^/]+)$ ]]; then
    owner=${BASH_REMATCH[1]}
    repo=${BASH_REMATCH[2]}
  elif [[ $url =~ ^ssh://git@github\.com/([^/]+)/([^/]+)$ ]]; then
    owner=${BASH_REMATCH[1]}
    repo=${BASH_REMATCH[2]}
  else
    echo "Remote ${remote} is not a GitHub SSH URL: ${url}" >&2
    return 1
  fi

  repo=${repo%.git}
  new_url="https://github.com/${owner}/${repo}.git"

  echo "Changing ${remote} from ${url} to ${new_url}"
  git remote set-url "$remote" "$new_url"
}
