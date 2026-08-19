// snippet:
// title: "Get the real client IP address"
// card_title: "Get the real client IP"
// summary: "Walk common proxy headers and REMOTE_ADDR, then return the first public IP that is not private or reserved, or Unknown if none validate."
// tags: [ip]
// added: "2026-08-19T11:16:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Forwarded headers can be spoofed. Private and reserved addresses are skipped, so local or LAN clients often return Unknown."
// end-snippet
function get_real_ip()
{
    foreach (array('HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_FORWARDED', 'HTTP_X_CLUSTER_CLIENT_IP', 'HTTP_FORWARDED_FOR', 'HTTP_FORWARDED', 'REMOTE_ADDR') as $key) {
        if (array_key_exists($key, $_SERVER) === true) {
            foreach (explode(',', $_SERVER[$key]) as $ip) {
                $ip = trim($ip);

                if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE) !== false) {
                    return $ip;
                }
            }
        }
    }
    return 'Unknown';
}
