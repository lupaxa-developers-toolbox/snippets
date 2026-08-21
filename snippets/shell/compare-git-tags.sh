# snippet:
# title: "Compare local and remote git tags"
# card_title: "Compare local remote tags"
# summary: "List tags that exist only locally or only on a remote after confirming the current directory is a git work tree."
# tags: [git]
# added: "2026-08-21T12:52:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs bash 4+ mapfile. Call compare_git_tags or compare_git_tags origin. ls-remote talks to the remote."
# end-snippet
compare_git_tags() {
  local remote=${1:-origin}
  local tag
  local -a local_tags=() remote_tags=() local_only=() remote_only=()
  local -A local_set=() remote_set=()

  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Not a git repository." >&2
    return 1
  fi

  if ! git remote get-url "$remote" >/dev/null 2>&1; then
    echo "Remote ${remote} is not configured." >&2
    return 1
  fi

  mapfile -t remote_tags < <(
    git ls-remote --tags --refs "$remote" | awk -F/ '{print $NF}' | sort -V
  )
  mapfile -t local_tags < <(git tag --list --sort=v:refname)

  for tag in "${local_tags[@]}"; do
    local_set[$tag]=1
  done
  for tag in "${remote_tags[@]}"; do
    remote_set[$tag]=1
  done

  for tag in "${local_tags[@]}"; do
    [[ -n ${remote_set[$tag]+x} ]] || local_only+=("$tag")
  done
  for tag in "${remote_tags[@]}"; do
    [[ -n ${local_set[$tag]+x} ]] || remote_only+=("$tag")
  done

  if ((${#local_only[@]} == 0 && ${#remote_only[@]} == 0)); then
    echo "Local and ${remote} tags match."
    return 0
  fi

  if ((${#local_only[@]} > 0)); then
    echo "Local only:"
    printf '  %s\n' "${local_only[@]}"
  fi
  if ((${#remote_only[@]} > 0)); then
    echo "Remote only (${remote}):"
    printf '  %s\n' "${remote_only[@]}"
  fi
}
