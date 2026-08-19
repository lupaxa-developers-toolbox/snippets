# snippet:
# title: "Rollback stack on interrupt or error"
# card_title: "Rollback on error"
# summary: "Push cleanup functions onto a LIFO stack and run them if INT, TERM, or EXIT fires, so partial work can be undone."
# tags: [cleanup]
# added: "2026-08-18T19:55:15+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Call unset_traps after a clean finish or the EXIT trap will undo the work. Each rollback is invoked with the argument rollback."
# end-snippet
rollback_stack=( )

add_rollback() {
  rollback_stack[${#rollback_stack[*]}]=$1
}

run_rollbacks() {
  unset_traps

  printf '\nTrap Triggers - Running Rollbacks\n\n'

  while [ ${#rollback_stack[@]} -ge 1 ]; do
    ${rollback_stack[${#rollback_stack[@]}-1]} rollback
    unset "rollback_stack[${#rollback_stack[@]}-1]"
  done

  exit
}

set_traps() {
  trap run_rollbacks INT TERM EXIT
}

unset_traps() {
  trap - INT TERM EXIT
}
