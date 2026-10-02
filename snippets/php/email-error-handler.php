// snippet:
// title: "Email PHP Errors to an Address"
// card_title: "Email PHP Errors"
// summary: "Register an error handler that emails the number, file, line, and message to a chosen address, then stops on anything more severe than a notice."
// tags: [email]
// added: "2026-10-02T17:41:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Set error_mail_to before registering the handler. error_log type 1 needs a working mail setup. Notices are emailed and the script continues. PHP 8 does not pass local variables into the handler. The last line triggers an undefined-variable notice."
// end-snippet
$error_mail_to = 'errors@example.com';

function email_error_handler($number, $message, $file, $line, $vars = null)
{
    global $error_mail_to;

    $email = "
        <p>An error ($number) occurred on line
        <strong>$line</strong> and in the <strong>file: $file.</strong>
        <p> $message </p>";

    if ($vars !== null) {
        $email .= '<pre>' . print_r($vars, true) . '</pre>';
    }

    $headers = 'Content-type: text/html; charset=iso-8859-1' . "\r\n";

    error_log($email, 1, $error_mail_to, $headers);

    if (($number !== E_NOTICE) && ($number < 2048)) {
        die('There was an error. Please try again later.');
    }
}

set_error_handler('email_error_handler');

echo $somevarthatdoesnotexist;
