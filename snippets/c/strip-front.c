// snippet:
// title: "Strip a character from the start of a string"
// card_title: "Strip from the front"
// summary: "Advance a pointer past every leading occurrence of a character and return the first position that is not that character."
// tags: [string]
// added: "2026-08-21T13:24:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Does not allocate or copy. NULL input returns NULL."
// end-snippet
char *stripfront(char *str, char c)
{
    if (str == NULL) {
        return NULL;
    }
    while (*str != '\0' && *str == c) {
        str++;
    }
    return str;
}
