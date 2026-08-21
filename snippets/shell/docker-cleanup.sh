# snippet:
# title: "Clean up unused Docker leftovers"
# card_title: "Clean up Docker leftovers"
# summary: "Remove exited and dead containers, containers stuck on untagged images, dangling images, and dangling volumes, or list them with -n."
# tags: [docker]
# added: "2026-08-21T12:50:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs docker on PATH. Call docker_cleanup or docker_cleanup -n. Does not prune unused networks or tagged images that are merely unused. Images still referenced by a container are left. Skips if docker rm is already running."
# end-snippet
docker_cleanup() {
  local dry_run=false
  local id image
  local -a ids

  case "${1:-}" in
    -n) dry_run=true ;;
    "") ;;
    *)
      echo "Usage: docker_cleanup [-n]" >&2
      return 1
      ;;
  esac

  if [[ $dry_run == false ]] && pgrep -f 'docker rm' >/dev/null 2>&1; then
    echo "docker rm already running; skipping." >&2
    return 0
  fi

  _docker_cleanup_apply() {
    local title=$1
    shift
    ids=()
    while IFS= read -r id; do
      [[ -n $id ]] && ids+=("$id")
    done
    echo "${title}:" >&2
    if ((${#ids[@]} == 0)); then
      echo "  (none)" >&2
      return 0
    fi
    if [[ $dry_run == true ]]; then
      printf '  %s\n' "${ids[@]}"
      return 0
    fi
    "$@" "${ids[@]}"
  }

  _docker_cleanup_apply "Exited and dead containers" docker rm -v < <(
    docker ps -aq -f status=exited
    docker ps -aq -f status=dead
  )

  _docker_cleanup_apply "Containers on untagged images" docker rm -v < <(
    while read -r id image; do
      [[ $image =~ ^[0-9a-f]+$ ]] && printf '%s\n' "$id"
    done < <(docker ps -a --format '{{.ID}} {{.Image}}')
  )

  _docker_cleanup_apply "Dangling images" docker rmi < <(
    docker images -qf dangling=true
  ) || true

  _docker_cleanup_apply "Dangling volumes" docker volume rm < <(
    docker volume ls -qf dangling=true
  ) || true

  unset -f _docker_cleanup_apply
}
