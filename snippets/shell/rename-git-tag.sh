# snippet:
# title: "Rename a local and remote git tag"
# card_title: "Rename a git tag"
# summary: "Point a new tag at the old one, delete the old name locally and on origin, then push tags so the renamed tag is published."
# tags: [git]
# added: "2026-08-19T16:14:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Call as rename_git_tag old new. git push --tags publishes every local tag. Anyone who already fetched the old name must delete it locally too."
# end-snippet
rename_git_tag() {
  local old=$1
  local new=$2

  git tag "$new" "$old"
  git tag -d "$old"
  git push origin ":refs/tags/${old}"
  git push --tags
}
