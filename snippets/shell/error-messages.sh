# snippet:
# title: "Coloured error, warning, and success lines"
# card_title: "Coloured messages"
# summary: "Print error, warning, and success lines in red, yellow, or green when the terminal supports colour, after get_colours has run."
# tags: [terminal, text]
# added: "2026-08-18T19:55:08+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Call get_colours before the show_* helpers."
# end-snippet
show_error() {
  if [[ -n $1 ]]; then
    printf '%s%s%s\n' "${red}" "${*}" "${reset}" 1>&2
  fi
}

show_warning() {
  if [[ -n $1 ]]; then
    printf '%s%s%s\n' "${yellow}" "${*}" "${reset}" 1>&2
  fi
}

show_success() {
  if [[ -n $1 ]]; then
    printf '%s%s%s\n' "${green}" "${*}" "${reset}" 1>&2
  fi
}

get_colours() {
  local ncolors

  red=''
  yellow=''
  green=''
  reset=''

  if ! test -t 1; then
    return
  fi

  if ! tput longname > /dev/null 2>&1; then
    return
  fi

  ncolors=$(tput colors)

  if ! test -n "${ncolors}" || test "${ncolors}" -le 7; then
    return
  fi

  red=$(tput setaf 1)
  yellow=$(tput setaf 3)
  green=$(tput setaf 2)
  reset=$(tput sgr0)

  readonly red yellow green reset
  declare -g red yellow green reset
}
