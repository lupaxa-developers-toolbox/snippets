# snippet:
# title: "Check a named path is a directory"
# card_title: "Check a directory exists"
# summary: "Return success if the named variable holds a path that exists as a directory."
# tags: [config]
# added: "2026-08-19T16:19:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Pass the variable name that stores the path, not the path itself."
# end-snippet
check_directory() {
  local dir_name=$1

  [[ -d "${!dir_name-}" ]]
}
