# snippet:
# title: "Check a named path is a live symlink"
# card_title: "Check a symlink exists"
# summary: "Return success if the named variable holds a path that is a symlink and whose target exists."
# tags: [config]
# added: "2026-08-19T16:19:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Pass the variable name that stores the path. Broken links fail."
# end-snippet
check_symlink() {
  local link_name=$1

  [[ -L "${!link_name-}" && -e "${!link_name-}" ]]
}
