# snippet:
# title: "Check a named path has given mode bits"
# card_title: "Check file permissions"
# summary: "Return success if the named path exists and its mode bits match the expected octal permissions, using GNU or BSD stat."
# tags: [config]
# added: "2026-08-19T16:19:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Pass the variable name that stores the path, then the expected mode as octal (for example 644)."
# end-snippet
check_permissions() {
  local file_name=$1
  local expected_perms=$2
  local actual_perms

  [[ -e "${!file_name-}" ]] || return 1

  actual_perms=$(stat -c "%a" "${!file_name}" 2>/dev/null || stat -f "%OLp" "${!file_name}" 2>/dev/null)
  [[ "$actual_perms" == "$expected_perms" ]]
}
