# snippet:
# title: Retry a callable
# card_title: "Retry a callable"
# summary: "Re-call a function with exponential backoff until it succeeds or reaches a retry limit, sleeping longer after each failed attempt."
# tags: [retry]
# added: "2026-08-18T18:03:20+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: Not for functions that are not idempotent.
# end-snippet

from collections.abc import Callable
from time import sleep
from typing import TypeVar

T = TypeVar("T")


def retry(func: Callable[[], T], attempts: int = 5, delay: float = 1.0) -> T:
    last: BaseException | None = None
    current = delay
    for _ in range(attempts):
        try:
            return func()
        except Exception as exc:  # noqa: BLE001 — caller decides what to retry
            last = exc
            sleep(current)
            current *= 2
    assert last is not None
    raise last
