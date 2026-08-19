# snippet:
# title: "Parse a URL into its parts"
# card_title: "Parse a URL"
# summary: "Split a URL into protocol, user, password, host, port, path, query, and fragment using bash parameter expansion, including user:password@ and host:port."
# tags: [url]
# added: "2026-08-19T16:23:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Fills the global associative array url_parts. Needs bash 4+. Do not log url_parts[pass]. Bracketed IPv6 with a port is supported; unbracketed IPv6 is treated as a host with no port."
# end-snippet
parse_url() {
  local url=$1
  local auth hostport

  url="${url#"${url%%[![:space:]]*}"}"
  url="${url%"${url##*[![:space:]]}"}"

  declare -gA url_parts=()

  if [[ $url == *://* ]]; then
    url_parts[proto]="${url%%://*}://"
    url="${url#*://}"
  fi

  if [[ $url == *#* ]]; then
    url_parts[fragment]="${url#*#}"
    url="${url%%#*}"
  fi

  if [[ $url == *\?* ]]; then
    url_parts[qs]="${url#*\?}"
    url="${url%%\?*}"
  fi

  if [[ $url == *@* ]]; then
    auth="${url%%@*}"
    url="${url#*@}"
    if [[ $auth == *:* ]]; then
      url_parts[user]="${auth%%:*}"
      url_parts[pass]="${auth#*:}"
    else
      url_parts[user]=$auth
    fi
  fi

  if [[ $url == */* ]]; then
    hostport="${url%%/*}"
    url_parts[path]="${url#*/}"
  else
    hostport=$url
  fi

  if [[ $hostport == \[*\]:* ]]; then
    url_parts[host]="${hostport%:*}"
    url_parts[port]="${hostport##*:}"
  elif [[ $hostport == *:* && $hostport != *:*:* ]]; then
    url_parts[host]="${hostport%:*}"
    url_parts[port]="${hostport##*:}"
  else
    url_parts[host]=$hostport
  fi
}
