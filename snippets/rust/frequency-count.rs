// snippet:
// title: "Count how often each item appears"
// card_title: "Count frequencies"
// summary: "Fold a slice into a HashMap that maps each value to how many times it occurs, incrementing the entry on each pass."
// tags: [count]
// added: "2026-08-21T13:29:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Needs T: Copy + Eq + Hash. Use Clone instead of Copy if the items are not Copy."
// end-snippet
use std::collections::HashMap;
use std::hash::Hash;

fn frequency_count<T: Copy + Eq + Hash>(items: &[T]) -> HashMap<T, usize> {
    items.iter().fold(HashMap::new(), |mut acc, &item| {
        *acc.entry(item).or_insert(0) += 1;
        acc
    })
}
