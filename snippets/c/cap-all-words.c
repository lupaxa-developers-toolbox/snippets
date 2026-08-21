// snippet:
// title: "Capitalise the first letter of each word"
// card_title: "Capitalise each word"
// summary: "Allocate a copy that uppercases the first letter after each space and lowercases the rest, or NULL if allocation fails."
// tags: [string]
// added: "2026-08-21T13:24:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Words are split only on space, not other whitespace. Caller must free the result. Needs ctype.h, stdlib.h, and string.h."
// end-snippet
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

char *cap_all_words(const char *str)
{
    size_t i;
    size_t n;
    char *buffer;
    int space = 0;

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
        if (space) {
            space = (str[i] == ' ');
            buffer[i] = (char)toupper((unsigned char)str[i]);
        } else {
            buffer[i] = (char)tolower((unsigned char)str[i]);
        }
        if (i + 1 < n && str[i + 1] == ' ') {
            space = 1;
        }
    }
    buffer[n] = '\0';
    return buffer;
}
