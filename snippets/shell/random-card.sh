# snippet:
# title: "Draw a random card from a 52-card deck"
# card_title: "Random playing card"
# summary: "Build a 52-card deck of ranks and suits, then print one card at random. The deck array is meant to sit beside other small game helpers."
# tags: [games]
# added: "2026-08-19T16:12:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs bash arrays and RANDOM. load_deck fills the global deck array."
# end-snippet
load_deck() {
  deck=()
  local suit rank

  for suit in clubs diamonds hearts spades; do
    for rank in ace 2 3 4 5 6 7 8 9 10 jack queen king; do
      deck+=("$rank of $suit")
    done
  done
}

load_deck
echo "${deck[RANDOM % ${#deck[@]}]}"
