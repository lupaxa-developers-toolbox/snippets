# snippet:
# title: "Center text on the terminal"
# card_title: "Center terminal text"
# summary: "Print a line padded with spaces so the text sits in the middle of the current terminal width, using tput for the column count."
# tags: [terminal, text]
# added: "2026-08-18T19:55:03+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Call get_screen_width first, or set screen_width yourself. Requires tput."
# end-snippet
center_text() {
  textsize=${#1}
  span=$(((screen_width + textsize) / 2))

  printf '%*s\n' "${span}" "$1"
}

get_screen_width() {
  screen_width=$(tput cols)
  declare -g screen_width
}
