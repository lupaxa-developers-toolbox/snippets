// snippet:
// title: "FizzBuzz by matching remainders"
// card_title: "FizzBuzz with tuples"
// summary: "Print Fizz, Buzz, or FizzBuzz by matching the pair of remainders modulo 3 and 5, and print the number when neither divides it."
// tags: [puzzle]
// added: "2026-08-21T13:28:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Change 1..=20 for a different range."
// end-snippet
for i in 1..=20 {
    match (i % 3, i % 5) {
        (0, 0) => println!("FizzBuzz"),
        (0, _) => println!("Fizz"),
        (_, 0) => println!("Buzz"),
        _ => println!("{i}"),
    }
}
