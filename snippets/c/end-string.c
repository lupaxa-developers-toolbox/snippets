// snippet:
// title: "Pointer one past a C string"
// card_title: "End of a string"
// summary: "Return a pointer to the byte after the terminating NUL of a C string, the one-past-end position."
// tags: [string]
// added: "2026-08-21T13:24:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Needs string.h. The result is not a valid C string. NULL input returns NULL."
// end-snippet
#include <string.h>

char *end_string(char *str)
{
    if (str == NULL) {
        return NULL;
    }
    str = strchr(str, '\0');
    str++;
    return str;
}
