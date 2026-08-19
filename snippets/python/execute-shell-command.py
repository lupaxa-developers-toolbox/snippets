# snippet:
# title: "Run a command and capture output"
# card_title: "Capture command output"
# summary: "Run an argv list as a subprocess and return the exit status together with captured stdout and stderr as strings."
# tags: [shell]
# added: "2026-08-18T19:55:34+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
import os
from subprocess import PIPE, Popen
from typing import Any, List, NamedTuple


class ExecutionResult(NamedTuple):
    status: int
    stdout: str
    stderr: str


def execute_shell_command(cmd: List[str]) -> ExecutionResult:
    with Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=os.getcwd()) as process:
        stdout_raw, stderr_raw = process.communicate()
        status: int | Any = process.returncode

    stdout = stdout_raw.decode('utf-8').rstrip()
    stderr = stderr_raw.decode('utf-8').rstrip()
    return ExecutionResult(status, stdout, stderr)
