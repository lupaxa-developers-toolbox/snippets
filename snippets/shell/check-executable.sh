# snippet:
# title: "Check a named command is on PATH"
# card_title: "Check a command exists"
# summary: "Return success if the named variable holds a command that command -v can find on PATH."
# tags: [config]
# added: "2026-08-19T16:19:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Pass the variable name that stores the command, not the command itself."
# end-snippet
check_executable() {
  local cmd_name=$1

  command -v "${!cmd_name-}" &>/dev/null
}
