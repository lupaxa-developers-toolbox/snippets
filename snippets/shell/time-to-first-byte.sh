# snippet:
# title: "Measure Time to First Byte"
# card_title: "Time to First Byte"
# summary: "Call curl on a URL and print namelookup, connect, TTFB (time_starttransfer), and total time, optionally repeating the request."
# tags: [curl, http]
# added: "2026-09-22T09:45:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs curl. Follows redirects; TTFB includes redirect time. Cache-Control no-cache is only a request header. time_to_first_byte URL [count]."
# end-snippet
time_to_first_byte() {
  local url="${1:?url required}"
  local count="${2:-1}"
  local i

  if ((count < 1)); then
    echo "count must be at least 1" >&2
    return 1
  fi

  for ((i = 1; i <= count; i++)); do
    curl -sSL -o /dev/null -H 'Cache-Control: no-cache' -w \
      'lookup %{time_namelookup}  connect %{time_connect}  ttfb %{time_starttransfer}  total %{time_total}\n' \
      "$url" || return
  done
}
