# snippet:
# title: "Read a password without echoing it"
# card_title: "Read a password silently"
# summary: "Prompt for a password with read -s so the characters never appear on the terminal, then restore the cursor to a new line."
# tags: [password]
# added: "2026-08-19T16:13:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Leaves the value in password. Do not echo it or pass it on a command line. Needs bash read -s."
# end-snippet
printf 'Password: '
read -rs password
printf '\n'
