# snippet:
# title: "Shuffle a Nested List or Tuple"
# card_title: "Shuffle a Nested List"
# summary: "Return a new list or tuple in random order, and shuffle nested lists or tuples down to a given depth."
# tags: [list]
# added: "2026-11-07T13:51:00+00:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Uses secrets.SystemRandom, so the order is not reproducible. Depth 1 shuffles only the outer sequence. Pass a higher depth to shuffle nested lists or tuples. Other types are left as they are."
# end-snippet
import secrets
from typing import Any

secrets_generator = secrets.SystemRandom()


def shuffled(things: Any, depth: int = 1) -> Any:
    if depth == 0 or not isinstance(things, (list, tuple)):
        return things

    results: list[Any] = []
    for item in things:
        if isinstance(item, (list, tuple)):
            results.append(shuffled(item, depth - 1))
        else:
            results.append(item)
    results = secrets_generator.sample(results, len(results))

    if isinstance(things, tuple):
        return tuple(results)
    return results


items_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, ["a", "b", "c"]]
items_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, ("a", "b", "c"))

items = items_tuple

print(items)
print(shuffled(items))
print(shuffled(items, 2))
print(items)
