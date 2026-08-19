# snippet:
# title: "Find the git work-tree root"
# card_title: "Find the git root"
# summary: "Print the top-level directory of a git work tree for the current or given path, or an error if that path is not a repository."
# tags: [git]
# added: "2026-08-18T19:55:10+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
get_git_root() {
  local root
  local retval

  (
    if [[ -n $1 ]]; then
      if [[ ! -d $1 ]]; then
        echo "$1 is not a valid directory"
        return 1
      fi
      cd "${1}" || return 1
    fi

    if git rev-parse --is-inside-git-dir > /dev/null 2>&1; then
      while [[ $(git rev-parse --is-inside-git-dir) == true ]]; do
        cd ..
      done
    fi

    if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
      root=$(git rev-parse --show-toplevel)
      retval=0
    else
      root="${PWD} is not a git repo"
      retval=1
    fi

    echo "${root}"
    return $retval
  )
}
