// snippet:
// title: "English ordinal form of a number"
// card_title: "Ordinal suffix"
// summary: "Return an integer with its English ordinal suffix, treating 11, 12, 13 and other teens as th, and 1, 2, 3 as st, nd, rd."
// tags: [text]
// added: "2026-08-21T13:27:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// end-snippet
fn get_ordinal(n: u32) -> String {
    let suffix = match (n % 10, n % 100) {
        (1, 11) | (2, 12) | (3, 13) => "th",
        (1, _) => "st",
        (2, _) => "nd",
        (3, _) => "rd",
        _ => "th",
    };
    format!("{n}{suffix}")
}
