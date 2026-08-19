# snippet:
# title: "Set terminal colour variables"
# card_title: "Terminal colour vars"
# summary: "Populate tput colour variables when stdout is a colour-capable terminal, and leave them empty so scripts stay readable in pipes."
# tags: [terminal, colour]
# added: "2026-08-18T19:55:21+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
set_colours() {
  fgRed=''
  fgYellow=''
  bgBlack=''
  bgWhite=''
  reset=''

  if test -t 1; then
    ncolors=$(tput colors)

    # shellcheck disable=SC2034
    if test -n "${ncolors}" && test "${ncolors}" -ge 8; then
      fgRed=$(tput setaf 1)
      fgYellow=$(tput setaf 3)
      bgBlack=$(tput setab 0)
      bgWhite=$(tput setab 7)
      reset=$(tput sgr0)
    fi
  fi
}
