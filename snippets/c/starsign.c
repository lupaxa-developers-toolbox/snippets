// snippet:
// title: "Star sign for a date, including cusps"
// card_title: "Star sign including cusps"
// summary: "Return an English star-sign name for a birthday, using a 24-name table that includes the cusp between neighbouring signs."
// tags: [date]
// added: "2026-08-21T13:18:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Month is 1-12. Invalid dates return Invalid Date. Cusp windows are the table in astro_offset, not IAU constellation dates."
// end-snippet
static int starsign_days_in_month(int month, int year)
{
    static const int days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    static const int leap_days[] = {31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int leap = (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;

    if (month < 1 || month > 12) {
        return 0;
    }
    return leap ? leap_days[month - 1] : days[month - 1];
}

static int astro_offset(int day, int month, int year)
{
    static const int cusp_start[12] = {17, 16, 19, 18, 18, 19, 19, 18, 18, 19, 19, 19};
    static const int cusp_end[12] = {22, 22, 23, 26, 22, 24, 24, 25, 23, 23, 24, 23};
    static const int cusp_offset[12] = {0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22};
    static const int normal[12] = {20, 19, 20, 20, 21, 21, 23, 23, 23, 23, 22, 21};
    static const int normal_offset[12] = {23, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21};

    if (month < 1 || month > 12 || day < 1 || day > starsign_days_in_month(month, year)) {
        return -1;
    }
    month--;

    if (day >= cusp_start[month] && day <= cusp_end[month]) {
        return cusp_offset[month];
    }
    if (day < normal[month]) {
        return normal_offset[month];
    }
    month++;
    if (month >= 12) {
        month = 0;
    }
    return normal_offset[month];
}

const char *starsign(int day, int month, int year)
{
    static const char *starsigns[24] = {
        "Capricorn/Aquarius (cusp)",
        "Aquarius",
        "Aquarius/Pisces (cusp)",
        "Pisces",
        "Pisces/Aries (cusp)",
        "Aries",
        "Aries/Taurus (cusp)",
        "Taurus",
        "Taurus/Gemini (cusp)",
        "Gemini",
        "Gemini/Cancer (cusp)",
        "Cancer",
        "Cancer/Leo (cusp)",
        "Leo",
        "Leo/Virgo (cusp)",
        "Virgo",
        "Virgo/Libra (cusp)",
        "Libra",
        "Libra/Scorpio (cusp)",
        "Scorpio",
        "Scorpio/Sagittarius (cusp)",
        "Sagittarius",
        "Sagittarius/Capricorn (cusp)",
        "Capricorn",
    };
    int offset = astro_offset(day, month, year);

    if (offset == -1) {
        return "Invalid Date";
    }
    return starsigns[offset];
}
