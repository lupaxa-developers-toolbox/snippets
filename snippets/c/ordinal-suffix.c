// snippet:
// title: "English ordinal suffix for an integer"
// card_title: "Ordinal suffix"
// summary: "Return st, nd, rd, or th for an integer, treating 11, 12, and 13 as th."
// tags: [string]
// added: "2026-08-21T13:24:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Only the values 11-19 use the teen rule. 111 returns st because the check is not applied to 111."
// end-snippet
const char *ord(int value)
{
    if (value > 10 && value < 20) {
        return "th";
    }
    switch (value % 10) {
    case 1:
        return "st";
    case 2:
        return "nd";
    case 3:
        return "rd";
    default:
        return "th";
    }
}
