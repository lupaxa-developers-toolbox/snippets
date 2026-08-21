// snippet:
// title: "Insert thousands separators in a number"
// card_title: "Comma-separate a number"
// summary: "Allocate a decimal string for an integer with commas every three digits, keeping a leading minus when the value is negative."
// tags: [string]
// added: "2026-08-21T13:24:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Caller must free the result. Uses a comma, not a locale thousands separator. Needs stdio.h and stdlib.h."
// end-snippet
#include <stdio.h>
#include <stdlib.h>

static int numdigits(int n)
{
    int count = 0;

    if (n == 0) {
        return 1;
    }
    while (n != 0) {
        n /= 10;
        ++count;
    }
    return count;
}

char *commify(int i)
{
    int len;
    int commas;
    int ign_dig;
    int count;
    int loop;
    char *tmp;
    char *ret;
    char *ptr;
    char *ptr2;

    len = numdigits(i);
    tmp = calloc(1, (size_t)len + 2);
    if (tmp == NULL) {
        return NULL;
    }
    sprintf(tmp, "%d", i);
    ptr = tmp;

    ign_dig = len % 3;
    commas = len / 3;
    if (ign_dig == 0) {
        commas--;
        if (commas < 0) {
            commas = 0;
        }
        ign_dig = 3;
    }

    ret = calloc(1, (size_t)len + (size_t)commas + 2);
    if (ret == NULL) {
        free(tmp);
        return NULL;
    }
    ptr2 = ret;
    if (*ptr == '-') {
        *ptr2++ = *ptr++;
    }
    for (count = 0; count < ign_dig; count++) {
        *ptr2++ = *ptr++;
    }
    for (loop = 0; loop < commas; loop++) {
        *ptr2++ = ',';
        for (count = 0; count < 3; count++) {
            *ptr2++ = *ptr++;
        }
    }
    while (*ptr != '\0') {
        *ptr2++ = *ptr++;
    }
    *ptr2 = '\0';
    free(tmp);
    return ret;
}
