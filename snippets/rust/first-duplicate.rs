// snippet:
// title: "Find the first duplicate value"
// card_title: "First duplicate"
// summary: "Walk a slice and return the first value that is already in a HashSet, using insert's false-on-duplicate result inside find."
// tags: [duplicates]
// added: "2026-08-21T13:29:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Needs T: Copy + Eq + Hash. Returns None when every value is unique."
// end-snippet
use std::collections::HashSet;
use std::hash::Hash;

fn first_duplicate<T: Copy + Eq + Hash>(items: &[T]) -> Option<T> {
    let mut seen = HashSet::new();
    items.iter().copied().find(|x| !seen.insert(*x))
}
