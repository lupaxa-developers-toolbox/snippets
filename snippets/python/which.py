# snippet:
# title: "Locate a command on PATH"
# card_title: "Locate a command"
# summary: "Search PATH for an executable name and return its expanded filesystem path, or a not-installed marker when nothing matches."
# tags: [path]
# added: "2026-08-18T19:55:39+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
import os
import shutil
from typing import Optional


def generate_expanded_path() -> str:
    current_path = os.environ.get('PATH', '')
    path_elements = current_path.split(os.pathsep)
    expanded = [os.path.expanduser(path) for path in path_elements]
    return os.pathsep.join(expanded)


def which(command: str) -> str:
    full_path: Optional[str] = shutil.which(command, path=generate_expanded_path())
    if full_path is None:
        return "not installed"
    return full_path
