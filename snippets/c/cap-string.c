// snippet:
// title: "Capitalise the first letter of a string"
// card_title: "Capitalise a string"
// summary: "Allocate a copy with the first character uppercased and the rest lowercased, or NULL if allocation fails."
// tags: [string]
// added: "2026-08-21T13:24:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Caller must free the result. Empty string returns an empty allocation. Needs ctype.h, stdlib.h, and string.h."
// end-snippet
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

char *cap_string(const char *str)
{
    size_t i;
    size_t n;
    char *buffer;

    if (str == NULL) {
        return NULL;
    }
    n = strlen(str);
    buffer = malloc(n + 1);
    if (buffer == NULL) {
        return NULL;
    }
    if (n == 0) {
        buffer[0] = '\0';
        return buffer;
    }
    buffer[0] = (char)toupper((unsigned char)str[0]);
    for (i = 1; i < n; i++) {
        buffer[i] = (char)tolower((unsigned char)str[i]);
    }
    buffer[n] = '\0';
    return buffer;
}
