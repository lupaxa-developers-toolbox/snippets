# snippet:
# title: "Convert a Netmask to a CIDR Prefix"
# card_title: "Netmask to CIDR Prefix"
# summary: "Return /N for a dotted IPv4 netmask, and reject masks whose 1-bits are not a contiguous prefix."
# tags: [network, cidr]
# added: "2026-09-09T16:42:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs bash. Prints /0 for 0.0.0.0 and /32 for 255.255.255.255. 255.255.255.183 is not a valid mask and is rejected."
# end-snippet
ip_prefix_by_netmask() {
  local mask="${1:?netmask required}"
  local -a octets
  local octet mask_int expected bits=0 bit

  IFS=. read -r -a octets <<< "$mask"
  if ((${#octets[@]} != 4)); then
    printf 'invalid subnet mask: %s\n' "$mask" >&2
    return 1
  fi
  for octet in "${octets[@]}"; do
    if [[ ! "$octet" =~ ^[0-9]+$ ]] || ((octet > 255)); then
      printf 'invalid subnet mask: %s\n' "$mask" >&2
      return 1
    fi
  done

  mask_int=$(((octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]))
  for ((bit = 31; bit >= 0; bit--)); do
    if ((((mask_int >> bit) & 1) == 0)); then
      break
    fi
    bits=$((bits + 1))
  done

  if ((bits == 0)); then
    expected=0
  else
    expected=$(((0xffffffff << (32 - bits)) & 0xffffffff))
  fi
  if ((mask_int != expected)); then
    printf 'invalid subnet mask: %s\n' "$mask" >&2
    return 1
  fi

  printf '/%s\n' "$bits"
}
