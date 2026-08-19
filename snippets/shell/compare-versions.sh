# snippet:
# title: "Compare version strings"
# card_title: "Compare versions"
# summary: "Compare two numeric version strings and return 0 if they are equal, 1 if the first is greater, or 2 if it is less."
# tags: [version]
# added: "2026-08-18T19:55:05+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Numeric components only. Optional third argument sets the delimiter (default is a dot)."
# end-snippet
compare_versions() {
  if [[ $1 == "${2}" ]]; then
    return 0
  fi

  if (($# == 3)); then
    IFS=$3
  else
    IFS=.
  fi

  local i ver1 ver2

  read -r -a ver1 <<< "${1}"
  read -r -a ver2 <<< "${2}"

  max=$(( ${#ver1[@]} > ${#ver2[@]} ? ${#ver1[@]} : ${#ver2[@]} ))

  for ((i = 0; i < max; i++)); do
    if ((10#${ver1[i]:-0} < 10#${ver2[i]:-0})); then
      return 2
    elif ((10#${ver1[i]:-0} > 10#${ver2[i]:-0})); then
      return 1
    fi
  done
  return 0
}
