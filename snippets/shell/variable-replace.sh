# snippet:
# title: "Replace placeholders from an associative array"
# card_title: "Replace placeholders"
# summary: "Substitute each key from a nameref associative array with its value inside a file, using in-place sed for the replacements."
# tags: [text]
# added: "2026-08-18T19:55:23+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "sed -i '' is the macOS in-place form. On GNU sed use sed -i. Keys are used as regexes."
# end-snippet
ref_array() {
  local varname="$1"
  local export_as="$2"
  local code

  code=$(declare -p "$varname")
  echo "${code/$varname/$export_as}"
}

replace_variables() {
  eval "$(ref_array "$1" array)"
  filename="${2}"

  local i search replace

  # shellcheck disable=SC2154
  for i in "${!array[@]}"; do
    search="${i}"
    replace="${array[$i]}"

    if grep -q "${search}" "${filename}"; then
      sed -i '' "s/${search}/${replace}/g" "${filename}"
      printf "Replaced %s with %s\n" "${search}" "${replace}"
    fi
  done
}
