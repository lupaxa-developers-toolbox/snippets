// snippet:
// title: "Days in a calendar month"
// card_title: "Days in a month"
// summary: "Return how many days a month has, using 29 for February in a Gregorian leap year and 0 when the month is out of range."
// tags: [date]
// added: "2026-08-21T13:16:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Month is 1-12. Needs is_leap_year from the Gregorian leap year snippet."
// end-snippet
int days_in_a_month(int month, int year)
{
    static const int days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    static const int leap_days[] = {31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    if (month < 1 || month > 12) {
        return 0;
    }
    return is_leap_year(year) ? leap_days[month - 1] : days[month - 1];
}
