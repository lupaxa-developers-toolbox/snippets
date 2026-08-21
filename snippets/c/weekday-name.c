// snippet:
// title: "Weekday name for a calendar date"
// card_title: "Weekday name"
// summary: "Return the weekday as a 0-Sunday index or as a short or long English name for a day, month, and year."
// tags: [date]
// added: "2026-08-21T13:19:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Month is 1-12. Weekday 0 is Sunday. Out-of-range day returns ERROR. Needs days_in_a_month from the days-in-a-month snippet."
// end-snippet
static const char *day_name_short[7] = {
    "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
};

static const char *day_name_long[7] = {
    "Sunday", "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday"
};

int day_of_the_week(int day, int month, int year)
{
    static const int t[] = {0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4};

    if (month < 1 || month > 12) {
        return -1;
    }
    year -= month < 3;
    return (year + year / 4 - year / 100 + year / 400 + t[month - 1] + day) % 7;
}

const char *long_day_of_the_week(int day, int month, int year)
{
    if (day < 1 || day > days_in_a_month(month, year)) {
        return "ERROR";
    }
    return day_name_long[day_of_the_week(day, month, year)];
}

const char *short_day_of_the_week(int day, int month, int year)
{
    if (day < 1 || day > days_in_a_month(month, year)) {
        return "ERROR";
    }
    return day_name_short[day_of_the_week(day, month, year)];
}
