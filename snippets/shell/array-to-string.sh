# snippet:
# title: "Join an array to a string"
# card_title: "Join an array"
# summary: "Join nameref array values with a separator, and optionally use a different separator before the last item for natural-language lists."
# tags: [array, text]
# added: "2026-08-18T19:55:02+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs Bash namerefs (Bash 4.3+). Pass the array name as the second argument."
# end-snippet
array_to_string() {
  separator="$1"
  local -n arr=$2

  regex="$( printf "${separator}%s" "${arr[@]}" )"
  regex="${regex:${#separator}}"

  if [[ -n $3 ]]; then
    if [[ $regex = *"$separator"* ]]; then
      prefix=${regex%"$separator"*}
      suffix=${regex#"$prefix"}
      regex=${prefix}${suffix/"$separator"/"$3"}
    fi
  fi

  echo "${regex}"
}
