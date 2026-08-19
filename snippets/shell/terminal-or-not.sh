# snippet:
# title: "Detect TTY, pipe, or redirect"
# card_title: "Detect TTY or redirect"
# summary: "Report whether stdout is attached to a terminal, a pipe, or a redirection so scripts can choose human or machine output."
# tags: [terminal]
# added: "2026-08-18T19:55:19+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
in_terminal() {
  [[ -t 1 ]] && return 0 || return 1
}

in_pipe() {
  [[ -p /dev/stdout ]] && return 0 || return 1
}

in_redirection() {
  [[ ! -t 1 && ! -p /dev/stdout ]] && return 0 || return 1
}
