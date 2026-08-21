// snippet:
// title: "Replace one substring with another"
// card_title: "Replace a substring"
// summary: "Allocate a copy of a string with each case-insensitive match of from replaced by to, or only the first match when single is set."
// tags: [string]
// added: "2026-08-21T13:24:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Caller must free the result. An empty from is left unchanged. Needs ctype.h, stdlib.h, and string.h."
// end-snippet
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

static const char *find_nocase(const char *haystack, const char *needle)
{
    size_t n;

    if (haystack == NULL || needle == NULL || *needle == '\0') {
        return NULL;
    }
    n = strlen(needle);
    for (; *haystack != '\0'; haystack++) {
        size_t i;
        for (i = 0; i < n; i++) {
            unsigned char a = (unsigned char)haystack[i];
            unsigned char b = (unsigned char)needle[i];

            if (haystack[i] == '\0' || tolower(a) != tolower(b)) {
                break;
            }
        }
        if (i == n) {
            return haystack;
        }
    }
    return NULL;
}

char *substr(const char *src, const char *from, const char *to, int single)
{
    size_t size;
    size_t fromlen;
    size_t tolen;
    char *ret;
    char *dst;

    if (src == NULL || from == NULL || to == NULL) {
        return NULL;
    }
    if (*from == '\0') {
        return strdup(src);
    }

    size = strlen(src) + 1;
    fromlen = strlen(from);
    tolen = strlen(to);
    ret = calloc(1, size);
    if (ret == NULL) {
        return NULL;
    }
    dst = ret;

    for (;;) {
        const char *match = find_nocase(src, from);

        if (match != NULL) {
            size_t count = (size_t)(match - src);
            char *temp;

            size += tolen - fromlen;
            temp = realloc(ret, size);
            if (temp == NULL) {
                free(ret);
                return NULL;
            }
            dst = temp + (dst - ret);
            ret = temp;
            memmove(dst, src, count);
            src += count;
            dst += count;
            memmove(dst, to, tolen);
            src += fromlen;
            dst += tolen;
            if (single) {
                strcpy(dst, src);
                break;
            }
        } else {
            strcpy(dst, src);
            break;
        }
    }
    return ret;
}
