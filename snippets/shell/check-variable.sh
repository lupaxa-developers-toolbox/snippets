# snippet:
# title: "Check a Named Variable is Set"
# card_title: "Check a Variable is Set"
# summary: "Return success if the named variable is set to a non-empty value, using indirect expansion so callers pass the variable name."
# tags: [config]
# added: "2026-08-19T16:19:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Pass the variable name, not its value. Empty and unset both fail."
# end-snippet
check_variable() {
  local var_name=$1

  [[ -n "${!var_name-}" ]]
}
