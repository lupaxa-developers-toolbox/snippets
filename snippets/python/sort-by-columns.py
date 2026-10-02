# snippet:
# title: "Sort Items by Several Columns"
# card_title: "Sort by Several Columns"
# summary: "Sort mappings by column names. A leading minus on a name sorts that column descending."
# tags: [list]
# added: "2026-10-02T17:49:00+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Each item must be a mapping with the named columns. Later columns break ties in earlier ones. A leading minus sorts that column descending."
# end-snippet
from functools import cmp_to_key
from operator import itemgetter
from typing import Any


def multikeysort(items: list[dict[str, Any]], columns: list[str]) -> list[dict[str, Any]]:
    comparers = [
        (itemgetter(col[1:].strip()), -1) if col.startswith("-") else (itemgetter(col.strip()), 1)
        for col in columns
    ]

    def comparer(left: dict[str, Any], right: dict[str, Any]) -> int:
        for fn, mult in comparers:
            left_value = fn(left)
            right_value = fn(right)
            result = (left_value > right_value) - (left_value < right_value)
            if result:
                return mult * result
        return 0

    return sorted(items, key=cmp_to_key(comparer))


results = [
    {"ParentType": "b", "ChildType": "a"},
    {"ParentType": "a", "ChildType": "b"},
]
sorted_results = multikeysort(results, ["ParentType", "ChildType"])
