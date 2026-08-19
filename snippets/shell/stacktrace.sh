# snippet:
# title: "Print a Bash stack trace"
# card_title: "Print a stack trace"
# summary: "Walk Bash caller frames from the current function back toward main and print each frame as a compact stack trace."
# tags: [debugging]
# added: "2026-08-18T19:55:16+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
stacktrace() {
  local start_from=${1:-0}
  local i=0

  while caller $i > /dev/null; do
    if (( "$i" + 1 >= "${start_from}" )); then
      caller $i
    fi
    ((i = i + 1))
  done
}
