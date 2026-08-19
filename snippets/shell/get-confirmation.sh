# snippet:
# title: "Ask until yes or no"
# card_title: "Ask until yes or no"
# summary: "Prompt until the user types y/yes or n/no, then echo 1 or 0 so the answer can be captured instead of using the exit status."
# tags: [interactive]
# added: "2026-08-18T19:55:09+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Unlike confirm(), this loops until y or n and prints 1 or 0 instead of using the exit status."
# end-snippet
get_confirmation() {
  local valid_response=false
  local return_value=0

  while [[ "$valid_response" = false ]]; do
    read -r -p "${1:-Are you sure? [y/N]} " response
    case $response in
      [yY][eE][sS]|[yY])
        valid_response=true
        return_value=1
        ;;
      [nN][oO]|[nN])
        valid_response=true
        return_value=0
        ;;
    esac
  done
  echo $return_value
}
