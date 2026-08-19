# snippet:
# title: "Ordinal suffix for a number"
# card_title: "Ordinal suffix"
# summary: "Return the English ordinal form of an integer, including the special cases 11th, 12th, and 13th as well as 1st, 2nd, and 3rd."
# tags: [text]
# added: "2026-08-18T19:55:36+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
from typing import Dict


def ordinal(num: int) -> str:
    suffixes: Dict[int, str] = {1: 'st', 2: 'nd', 3: 'rd'}

    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        suffix = suffixes.get(num % 10, 'th')

    return f"{num}{suffix}"
