// snippet:
// title: "Partition an array into N groups"
// card_title: "Partition an array"
// summary: "Split a list into p slices of roughly equal size, spreading any remainder across the first groups so lengths differ by at most one."
// tags: [array]
// added: "2026-08-18T19:55:30+01:00"
// submitted_by: Lupraxus
// runnable: false
// end-snippet
function partition_array($list, $p)
{
    $list_length = count($list);
    $partition_length = floor($list_length / $p);
    $partition_remainder = $list_length % $p;
    $partition = array();
    $mark = 0;
    for ($px = 0; $px < $p; $px++) {
        $increment = ($px < $partition_remainder) ? $partition_length + 1 : $partition_length;
        $partition[$px] = array_slice($list, $mark, $increment);
        $mark += $increment;
    }
    return $partition;
}
