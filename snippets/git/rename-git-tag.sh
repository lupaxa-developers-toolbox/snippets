# snippet:
# title: "Rename a Local and Remote Git Tag"
# card_title: "Rename a Git Tag"
# summary: "Point a new tag at the old one, delete the old name locally and on origin, then push tags so the renamed tag is published."
# tags: [git]
# added: "2026-08-19T16:14:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Replace <OLD> and <NEW>. git push --tags publishes every local tag. Anyone who already fetched the old name must delete it locally too."
# end-snippet
git tag <NEW> <OLD>
git tag -d <OLD>
git push origin ":refs/tags/<OLD>"
git push --tags
