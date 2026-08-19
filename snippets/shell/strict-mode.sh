# snippet:
# title: "Bash strict mode"
# card_title: "Bash strict mode"
# summary: "Enable errexit, nounset, pipefail, and a safer IFS, and turn on xtrace when DEBUG is set so failures stop the script early."
# tags: [robustness]
# added: "2026-08-18T19:55:17+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "grep -c and unset variables need || true and ${VAR:-} under these options."
# end-snippet
set -o errexit
set -o nounset
set -o pipefail
[[ -n ${DEBUG:-} ]] && set -o xtrace
IFS=$'\n\t'
