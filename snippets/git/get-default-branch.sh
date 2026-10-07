# snippet:
# title: "Get the Default Branch for a Repository"
# card_title: "Get Default Branch"
# summary: "Print the default branch name that origin reports as HEAD, trimmed of surrounding whitespace."
# tags: [git]
# added: "2026-10-07T14:28:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs a configured origin remote. git remote show talks to the remote."
# end-snippet
git remote show origin | grep 'HEAD' | cut -d':' -f2 | sed -e 's/^ *//g' -e 's/ *$//g'
