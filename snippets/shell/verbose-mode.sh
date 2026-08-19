# snippet:
# title: "Silent mode with a forced-output helper"
# card_title: "Silent mode helper"
# summary: "When VERBOSE is false, send stdout and stderr to /dev/null, while still allowing a forced-output helper to print essential lines."
# tags: [terminal]
# added: "2026-08-18T19:55:24+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Set VERBOSE before calling set_verbose_mode. Use output msg forced for lines that must always show."
# end-snippet
set_verbose_mode() {
  exec 3>&1
  exec 4>&2

  if [[ "${VERBOSE}" = true ]]; then
    echo "Verbose output enabled"
  else
    exec 1>/dev/null
    exec 2>/dev/null
  fi
}

output() {
  if [[ -n $1 ]]; then
    if [[ -n $2 ]] && [[ "${2}" = forced ]]; then
      echo "$1" 1>&3 2>&4
    else
      echo "$1"
    fi
  fi
}
