# snippet:
# title: "Check Prerequisite Commands Are Installed"
# card_title: "Check Prerequisites"
# summary: "Search an expanded PATH for each command name and return its full path, or raise when any name is missing."
# tags: [path]
# added: "2026-10-02T17:31:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Raises PrerequisiteCheckError with one message per missing command. PATH entries that start with ~ are expanded before the search."
# end-snippet
import os
import shutil


class PrerequisiteCheckError(Exception):
    def __init__(self, errors: list[str]) -> None:
        super().__init__("\n".join(errors))
        self.errors = errors


def generate_expanded_path() -> str:
    current_path: str = os.environ.get("PATH", "")
    path_elements: list[str] = current_path.split(os.pathsep)
    expanded_path_elements: list[str] = [os.path.expanduser(path) for path in path_elements]
    return os.pathsep.join(expanded_path_elements)


def check_prerequisite(prerequisite_commands: list[str]) -> dict[str, str]:
    errors_verbose: list[str] = []
    command_paths: dict[str, str] = {}
    expanded_search_path: str = generate_expanded_path()

    for command in prerequisite_commands:
        full_path: str | None = shutil.which(command, path=expanded_search_path)
        if full_path is None:
            errors_verbose.append(f"{command} is not installed")
        else:
            command_paths[command] = full_path

    if errors_verbose:
        raise PrerequisiteCheckError(errors_verbose)

    return command_paths
