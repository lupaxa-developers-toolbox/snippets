// snippet:
// title: "Test a Gregorian leap year"
// card_title: "Gregorian leap year"
// summary: "Return true when a year is a Gregorian leap year: divisible by 4, but not by 100 unless also divisible by 400."
// tags: [date]
// added: "2026-08-21T13:19:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Gregorian calendar only. Year is a full calendar year, not two digits."
// end-snippet
int is_leap_year(int year)
{
    return (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
}
