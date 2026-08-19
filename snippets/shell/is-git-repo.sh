# snippet:
# title: "Test whether a directory is a git work tree"
# card_title: "Test a git work tree"
# summary: "Return success if the current or given directory sits inside a git work tree, without printing the repository root."
# tags: [git]
# added: "2026-08-18T19:55:14+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
is_git_repo() {
  local retval

  (
    if [[ -n $1 ]]; then
      if [[ ! -d $1 ]]; then
        return 1
      fi
      cd "${1}" || return 1
    fi

    if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
      retval=0
    else
      retval=1
    fi
    return $retval
  )
}
