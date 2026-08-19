# snippet:
# title: "Absolute value"
# card_title: "Absolute value"
# summary: "Print the absolute value of an integer argument, stripping a leading minus so downstream scripts always see a non-negative number."
# tags: [math]
# added: "2026-08-18T19:55:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
abs() {
  (( $1 < 0 )) && echo "$(( $1 * -1 ))" || echo "$1"
}
