# snippet:
# title: "Lowercase filenames in the current directory"
# card_title: "Lowercase filenames"
# summary: "Rename each regular file in the current directory to lowercase and append the reverse mv to restore.sh so the original names can be put back."
# tags: [files]
# added: "2026-08-19T16:09:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Skips directories. Appends to restore.sh. A lowercase name that already exists will be overwritten. Run from the directory you want to rename."
# end-snippet
for file in *; do
  # Drop this test to lowercase directories as well.
  if [[ ! -f "$file" ]]; then
    continue
  fi

  lc_file=$(echo "$file" | tr '[:upper:]' '[:lower:]')
  if [[ "$file" != "$lc_file" ]]; then
    echo "mv $lc_file $file" >> restore.sh
    mv "$file" "$lc_file"
  fi
done
