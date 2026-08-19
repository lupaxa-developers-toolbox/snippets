# snippet:
# title: "Extract a numeric version from text"
# card_title: "Extract a version"
# summary: "Pull the first run of digits and dots out of a string so a human version line becomes a comparable numeric version."
# tags: [version, text]
# added: "2026-08-18T19:55:13+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
get_version_string() {
  raw_string="${1:-}"

  # shellcheck disable=SC2001
  version=$(echo "${raw_string}" | sed 's/[^0-9.]*\([0-9.]*\).*/\1/')
  echo "${version}"
}
