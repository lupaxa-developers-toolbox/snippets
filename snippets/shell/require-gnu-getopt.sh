# snippet:
# title: "Ensure GNU getopt is on PATH"
# card_title: "Require GNU getopt"
# summary: "Fail unless getopt --test exits 4, which only util-linux GNU getopt does, and point macOS users at brew gnu-getopt instead of BSD getopt."
# tags: [getopt]
# added: "2026-08-19T16:16:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "This is the external getopt binary, not bash getopts. Call require_gnu_getopt before parsing long options. brew install gnu-getopt on macOS."
# end-snippet
require_gnu_getopt() {
  local status=0

  getopt --test >/dev/null 2>&1 || status=$?
  if (( status == 4 )); then
    return 0
  fi

  if [[ "$(uname -s)" == Darwin ]]; then
    echo "macOS ships BSD getopt. Install GNU getopt (brew install gnu-getopt) and put it first on PATH." >&2
  else
    echo "'getopt --test' failed in this environment - please use GNU getopt." >&2
  fi
  exit 1
}
