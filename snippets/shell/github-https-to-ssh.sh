# snippet:
# title: "Switch a GitHub HTTPS remote to SSH"
# card_title: "HTTPS remote to SSH"
# summary: "Rewrite a GitHub HTTPS remote to a git@ SSH URL after checking the current directory is a git work tree."
# tags: [git]
# added: "2026-08-21T12:54:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "GitHub remotes only. Call github_https_to_ssh or github_https_to_ssh origin. Leaves the URL unchanged if it is already SSH."
# end-snippet
github_https_to_ssh() {
  local remote=${1:-origin}
  local url owner repo new_url
  local host=github.com
  local scheme=https

  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Not a git repository." >&2
    return 1
  fi

  if ! url=$(git remote get-url "$remote" 2>/dev/null); then
    echo "Remote ${remote} is not configured." >&2
    return 1
  fi

  if [[ $url == git@${host}:* || $url == ssh://git@${host}/* ]]; then
    echo "${remote} is already SSH: ${url}"
    return 0
  fi

  if [[ $url =~ ^${scheme}://${host//./\\.}/([^/]+)/([^/]+)$ ]]; then
    owner=${BASH_REMATCH[1]}
    repo=${BASH_REMATCH[2]}
  elif [[ $url =~ ^${scheme}://[^@/]+@${host//./\\.}/([^/]+)/([^/]+)$ ]]; then
    owner=${BASH_REMATCH[1]}
    repo=${BASH_REMATCH[2]}
  else
    echo "Remote ${remote} is not a GitHub HTTPS URL: ${url}" >&2
    return 1
  fi

  repo=${repo%.git}
  new_url="git@${host}:${owner}/${repo}.git"

  echo "Changing ${remote} from ${url} to ${new_url}"
  git remote set-url "$remote" "$new_url"
}
