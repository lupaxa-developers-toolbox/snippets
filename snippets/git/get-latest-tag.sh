# snippet:
# title: "Get the Latest Tag from a Repository URL"
# card_title: "Get Latest Tag"
# summary: "List version-sorted remote tags that match a dotted triple and print the highest name, skipping peeled annotated-tag objects."
# tags: [git]
# added: "2026-10-07T14:35:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Replace <REPO URL> with the remote. Talks to the remote. Only matches tags of the form *.*.*."
# end-snippet
git -c versionsort.suffix=- ls-remote --tags --sort=v:refname <REPO URL> '*.*.*' | awk -F/ '/refs\/tags\// && !/\^\{\}$/ {print $3}' | tail -n1
