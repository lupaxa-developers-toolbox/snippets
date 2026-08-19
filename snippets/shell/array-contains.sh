# snippet:
# title: "Array contains a value"
# card_title: "Array contains a value"
# summary: "Return success if a Bash nameref array contains a given value, or failure if the value is missing, without expanding the array yourself."
# tags: [array]
# added: "2026-08-18T19:55:01+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs Bash namerefs (Bash 4.3+). Pass the array name, not an expansion."
# end-snippet
array_contains() {
  local -n haystack=$1
  local needle=$2

  for i in "${haystack[@]}"; do
    if [[ $i == "${needle}" ]]; then
      return 0
    fi
  done

  return 1
}
