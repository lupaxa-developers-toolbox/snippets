// snippet:
// title: "Look up an array key"
// card_title: "Look up an array key"
// summary: "Look up a value by array key, with an optional case-insensitive search that still returns the original stored value."
// tags: [array]
// added: "2026-08-18T19:55:29+01:00"
// submitted_by: Lupraxus
// runnable: false
// end-snippet
function array_key_search($haystack, $needle)
{
    if (isset($haystack["$needle"])) {
        return $haystack["$needle"];
    }
    return null;
}

function array_key_isearch($haystack, $needle)
{
    $haystack = array_change_key_case($haystack, CASE_LOWER);
    $needle = strtolower($needle);

    return array_key_search($haystack, $needle);
}
