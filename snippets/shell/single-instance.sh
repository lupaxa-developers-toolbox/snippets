# snippet:
# title: "Allow only one running instance"
# card_title: "Single-instance lock"
# summary: "Take an exclusive flock on a /tmp lock file so a cron job or script exits instead of overlapping a previous run, with a noclobber fallback when flock is missing."
# tags: [lock, cron]
# added: "2026-08-19T11:10:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Replace actual_script with your work. The lock file is /tmp/<script-name>.lock. Without flock, the noclobber fallback is not atomic across all filesystems."
# end-snippet
# shellcheck disable=SC2155
readonly PROGNAME=$(basename "$0")
readonly LOCKFILE_DIR=/tmp
readonly LOCK_FD=200

actual_script() {
  echo "I am Locked - Sleep time"
  sleep 3
  echo "Now I Unlock"
}

lock() {
  local prefix=$1
  local fd=${2:-$LOCK_FD}
  local lock_file=$LOCKFILE_DIR/$prefix.lock

  if ! command -v flock >/dev/null 2>&1; then
    if (set -o noclobber; echo "$$" > "${lock_file}") 2>/dev/null; then
      # shellcheck disable=SC2064
      trap 'rm -f "${lock_file}"; exit $?' INT TERM EXIT
      return 0
    fi
    return 1
  fi

  eval "exec ${fd}>\"${lock_file}\""
  flock -n "${fd}"
}

eexit() {
  local message="${1:-}"

  if [[ -n "${message}" ]]; then
    echo "${message}"
  fi
  exit 1
}

wrapper() {
  lock "${PROGNAME}" || eexit "Only one instance of ${PROGNAME} can run at one time."
  actual_script
}

wrapper
