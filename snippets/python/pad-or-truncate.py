# snippet:
# title: "Pad or Truncate a List"
# card_title: "Pad or Truncate"
# summary: "Cut a list to a target length, or extend it with a fill value when it is shorter."
# tags: [list]
# added: "2026-10-02T17:47:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "The fill value is repeated by reference. Use an immutable fill such as a string. A negative target length slices from the end and does not pad."
# end-snippet
from typing import Any


def pad_or_truncate(items: list[Any], target_len: int, fill: Any = "N") -> list[Any]:
    return items[:target_len] + [fill] * (target_len - len(items))
