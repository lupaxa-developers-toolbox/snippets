# snippet:
# title: "Expand a Network Address to IPs"
# card_title: "Expand Network to IPs"
# summary: "Print every IPv4 address in a CIDR or dotted-mask network, including the network and broadcast addresses."
# tags: [network, cidr]
# added: "2026-09-09T16:41:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs bash. Includes network and broadcast. /0 enumerates 2^32 addresses. The address is masked to the network base first, so 10.0.0.5/24 lists 10.0.0.0-255."
# end-snippet
network_address_to_ips() {
  local spec="${1:?network/mask required}"
  local addr="${spec%%/*}"
  local mask="${spec#*/}"
  local -a ip octets
  local mask_int ip_int start end host_bits i octet

  [[ "$mask" == "$spec" ]] && mask=32

  IFS=. read -r -a ip <<< "$addr"
  if ((${#ip[@]} != 4)); then
    printf 'invalid IPv4 address: %s\n' "$addr" >&2
    return 1
  fi
  for octet in "${ip[@]}"; do
    if [[ ! "$octet" =~ ^[0-9]+$ ]] || ((octet > 255)); then
      printf 'invalid IPv4 address: %s\n' "$addr" >&2
      return 1
    fi
  done

  if [[ "$mask" == *.* ]]; then
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
  else
    if [[ ! "$mask" =~ ^[0-9]+$ ]] || ((mask > 32)); then
      printf 'invalid CIDR prefix: %s\n' "$mask" >&2
      return 1
    fi
    if ((mask == 0)); then
      mask_int=0
    else
      mask_int=$(((0xffffffff << (32 - mask)) & 0xffffffff))
    fi
  fi

  ip_int=$(((ip[0] << 24) + (ip[1] << 16) + (ip[2] << 8) + ip[3]))
  start=$((ip_int & mask_int))
  host_bits=$((0xffffffff ^ mask_int))
  end=$((start | host_bits))

  for ((i = start; i <= end; i++)); do
    printf '%d.%d.%d.%d\n' \
      $(((i >> 24) & 255)) \
      $(((i >> 16) & 255)) \
      $(((i >> 8) & 255)) \
      $((i & 255))
  done
}
