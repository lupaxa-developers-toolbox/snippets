# snippet:
# title: "Check a named path is a file"
# card_title: "Check a file exists"
# summary: "Return success if the named variable holds a path that exists as a regular file."
# tags: [config]
# added: "2026-08-19T16:19:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Pass the variable name that stores the path, not the path itself."
# end-snippet
check_file() {
  local file_name=$1

  [[ -f "${!file_name-}" ]]
}
