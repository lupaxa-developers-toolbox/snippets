# snippet:
# title: "Check a Named Localhost Port is Open"
# card_title: "Check a Port is Open"
# summary: "Return success if nc can connect to localhost on the TCP port stored in the named variable."
# tags: [config]
# added: "2026-08-19T16:19:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Pass the variable name that stores the port. Needs nc. Only probes localhost."
# end-snippet
check_port() {
  local port=$1

  nc -z localhost "${!port-}" &>/dev/null
}
