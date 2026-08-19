# snippet:
# title: "Check a named array is non-empty"
# card_title: "Check an array is set"
# summary: "Return success if the named array exists and contains at least one element, using a nameref so callers pass the array name."
# tags: [config]
# added: "2026-08-19T16:19:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Pass the array name, not its value. Needs bash nameref (4.3+)."
# end-snippet
check_array() {
  local arr_name=$1

  declare -p "$arr_name" &>/dev/null || return 1

  local -n arr=$arr_name
  (( ${#arr[@]} > 0 ))
}
