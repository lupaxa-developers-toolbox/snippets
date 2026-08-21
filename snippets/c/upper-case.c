// snippet:
// title: "Copy a string in uppercase"
// card_title: "Uppercase a string"
// summary: "Allocate an uppercase copy of a C string with toupper and return it, or NULL if allocation fails."
// tags: [string]
// added: "2026-08-21T13:24:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Caller must free the result. Needs ctype.h, stdlib.h, and string.h. NULL input returns NULL."
// end-snippet
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

char *upper_case(const char *str)
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
    for (i = 0; i < n; i++) {
        buffer[i] = (char)toupper((unsigned char)str[i]);
    }
    buffer[n] = '\0';
    return buffer;
}
