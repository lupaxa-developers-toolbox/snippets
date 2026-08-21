// snippet:
// title: "Approximate moon phase for a date"
// card_title: "Moon phase name"
// summary: "Return an English moon-phase name for a calendar date using a 19-year cycle approximation, not a full astronomical ephemeris."
// tags: [date]
// added: "2026-08-21T13:17:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Month is 1-12. Day 31 is treated as 1. This is a coarse 8-phase label, not a precise illumination."
// end-snippet
const char *moon_phase(int day, int month, int year)
{
    static const char *moon_description[8] = {
        "New Moon",
        "Waxing Crescent",
        "First Quarter",
        "Waxing Gibbous",
        "Full Moon",
        "Waning Gibbous",
        "Last Quarter",
        "Waning Crescent",
    };
    static const short ages[] = {
        18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7,
    };
    static const short offsets[] = {-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9};
    int phase;

    if (month < 1 || month > 12) {
        return "ERROR";
    }
    if (day == 31) {
        day = 1;
    }

    phase = (ages[(year + 1) % 19] + ((day + offsets[month - 1]) % 30) + (year < 1900)) % 30;
    phase = (int)((phase + 2) * 16L / 59L);
    if (phase > 7) {
        phase = 0;
    }
    return moon_description[phase];
}
