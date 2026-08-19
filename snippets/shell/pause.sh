# snippet:
# title: Pause until Enter
# card_title: "Pause until Enter"
# summary: "Block until the user presses Enter, then continue; treat end-of-file as a clean exit so piped input does not hang."
# tags: [interactive]
# added: "2026-08-18T19:16:01+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: Exits the whole process on EOF (for example Ctrl-D).
# end-snippet

pause() {
  printf "\nPress Enter to continue..."
  if ! read -r _; then
    printf "\nEOF; exiting.\n"
    exit 0
  fi
}
