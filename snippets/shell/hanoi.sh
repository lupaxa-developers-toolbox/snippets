# snippet:
# title: "Solve the Tower of Hanoi"
# card_title: "Tower of Hanoi solver"
# summary: "Print the moves that transfer n discs from peg 1 to peg 2 using peg 3 as spare, for n from 1 to 9."
# tags: [puzzle]
# added: "2026-08-19T16:06:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Pass the disc count as the first argument (1-9). Pegs are numbered 1, 2, and 3."
# end-snippet
hanoi() {
  local -i n=$1
  local from=$2
  local to=$3
  local spare=$4

  if (( n > 1 )); then
    hanoi $((n - 1)) "$from" "$spare" "$to"
  fi
  echo "Move from peg $from to peg $to"
  if (( n > 1 )); then
    hanoi $((n - 1)) "$spare" "$to" "$from"
  fi
}

case "${1:-}" in
  [1-9])
    hanoi "$1" 1 2 3
    ;;
  *)
    echo "${0##*/}: argument must be from 1 to 9" >&2
    exit 1
    ;;
esac
