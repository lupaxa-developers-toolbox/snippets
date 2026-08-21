// snippet:
// title: "Advance to the next run of a character"
// card_title: "Next matching character"
// summary: "Walk a string to the first occurrence of a character, then to the last character of that run, or to the terminator if it is missing."
// tags: [string]
// added: "2026-08-21T13:24:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Returns a pointer into the original string. NULL input returns NULL."
// end-snippet
char *next_char(char *str, char c)
{
    if (str == NULL) {
        return NULL;
    }
    while (*str != '\0' && *str != c) {
        str++;
    }
    if (*str == c) {
        while (*str == c) {
            str++;
        }
        str--;
    }
    return str;
}
