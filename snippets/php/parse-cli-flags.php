// snippet:
// title: "Parse Short and Long CLI Flags"
// card_title: "Parse CLI Flags"
// summary: "Parse help, version, aflag, and b from short or long flags, and return the values keyed by the long name."
// tags: [cli]
// added: "2026-10-02T17:38:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Reads the real process argv. help and version are switches. aflag is required and takes a value. b is optional and takes a value. Passing both forms of one option, or omitting aflag, prints an error and exits."
// end-snippet
function parse_args()
{
    $specs = array(
        array(
            'short' => 'h',
            'long' => 'help',
            'flag' => true,
            'required' => false,
        ),
        array(
            'short' => 'v',
            'long' => 'version',
            'flag' => true,
            'required' => false,
        ),
        array(
            'short' => 'a',
            'long' => 'aflag',
            'required' => true,
        ),
        array(
            'short' => 'b',
            'long' => 'b',
            'required' => false,
        ),
    );

    return parse_specs($specs);
}

function parse_specs($specs)
{
    $shortopts = '';
    $longopts = array();
    $opts = array();

    foreach ($specs as $spec) {
        if (!empty($spec['short'])) {
            $shortopts .= $spec['short'];
            if (empty($spec['flag'])) {
                $shortopts .= ':';
            }
        }
        if (!empty($spec['long'])) {
            $longopt = $spec['long'];
            if (empty($spec['flag'])) {
                $longopt .= ':';
            }
            $longopts[] = $longopt;
        }
    }

    $parsed = getopt($shortopts, $longopts);

    foreach ($specs as $spec) {
        $long = $spec['long'];
        $short = $spec['short'];

        if (array_key_exists($long, $parsed) && array_key_exists($short, $parsed)) {
            cli_spec_error('Inconsistent use of flag: ' . $long);
        }
        if (array_key_exists($long, $parsed)) {
            $opts[$long] = ($parsed[$long] == false ? true : $parsed[$long]);
        } elseif (array_key_exists($short, $parsed)) {
            $opts[$long] = ($parsed[$short] == false ? true : $parsed[$short]);
        } elseif ($spec['required'] == true) {
            cli_spec_error('Required option ' . $long . ' is not present.');
        }
    }

    return $opts;
}

function cli_spec_error($error_message)
{
    fwrite(STDERR, $error_message . "\n");
    exit(1);
}
