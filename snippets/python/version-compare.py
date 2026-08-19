# snippet:
# title: "Compare dotted version strings"
# card_title: "Compare versions"
# summary: "Compare two dotted numeric version strings and return a negative number, zero, or a positive number for less, equal, or greater."
# tags: [version]
# added: "2026-08-18T19:55:38+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
import re
from typing import List


def version_compare(version1: str, version2: str) -> int:
    def normalize(v: str) -> List[int]:
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]

    def cmp(left, right):
        return (left > right) - (left < right)

    return cmp(normalize(version1), normalize(version2))
