# snippet:
# title: "Check required commands exist"
# card_title: "Check required commands"
# summary: "Walk a COMMANDS list and exit with an error as soon as any required program name is missing from PATH."
# tags: [path]
# added: "2026-08-18T19:55:04+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Set COMMANDS to the list of command names to require before calling check_prereqs."
# end-snippet
check_prereqs() {
  local error_count=0

  for i in "${COMMANDS[@]}"; do
    command=$(command -v "${i}")
    if [[ -z $command ]]; then
      printf '%s is not in your command path\n' "${i}"
      error_count=$((error_count + 1))
    fi
  done

  if [[ $error_count -gt 0 ]]; then
    printf '%d errors located - fix before re-running\n' "${error_count}"
    exit 1
  fi
}
