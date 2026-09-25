// snippet:
// title: "Strip a Character from the End of a String"
// card_title: "Strip from the End"
// summary: "Overwrite trailing CR, LF, and a chosen character with NULs so the string no longer ends on those bytes."
// tags: [string]
// added: "2026-08-21T13:24:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Mutates the buffer in place. Empty and NULL strings are returned unchanged. Needs string.h."
// end-snippet
#include <string.h>

char *stripend(char *str, char c)
{
    char *ptr;

    if (str == NULL || *str == '\0') {
        return str;
    }
    ptr = strchr(str, '\0');
    ptr--;
    while (ptr >= str && (*ptr == '\n' || *ptr == '\r' || *ptr == c)) {
        *ptr-- = '\0';
    }
    return str;
}
