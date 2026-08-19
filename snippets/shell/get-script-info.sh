# snippet:
# title: "Record how a script was invoked"
# card_title: "Record script invocation"
# summary: "Record the current script's path, name, sourced-or-executed status, and arguments in variables for later logging or usage text."
# tags: [scripting]
# added: "2026-08-18T19:55:11+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Set READONLY_INFO=true before calling if the exported names should be readonly."
# end-snippet
get_script_info() {
  local ro=${READONLY_INFO:-false}

  [[ $0 != "${BASH_SOURCE[0]}" ]] && IS_SOURCED=true || IS_SOURCED=false

  READONLY=false
  INVOKED_FILE="${BASH_SOURCE[${#BASH_SOURCE[@]} - 1]}"
  INVOKED_PATH="$(dirname "${BASH_SOURCE[${#BASH_SOURCE[@]} - 1]}")"
  FULL_PATH="$( cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
  FILE_NAME=$(basename "${BASH_SOURCE[0]}")

  if [[ $# -gt 0 ]]; then
    SCRIPT_ARGS=$(printf "'%s', " "${@}")
    SCRIPT_ARGS=${SCRIPT_ARGS::-2}
  else
    SCRIPT_ARGS="None"
  fi

  if [[ "${ro}" = true ]]; then
    readonly IS_SOURCED INVOKED_FILE INVOKED_PATH FULL_PATH FILE_NAME SCRIPT_ARGS
  fi

  export READONLY IS_SOURCED INVOKED_FILE INVOKED_PATH FULL_PATH FILE_NAME SCRIPT_ARGS
}
