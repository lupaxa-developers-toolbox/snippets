# snippet:
# title: "Post a message to Slack"
# card_title: "Post a Slack message"
# summary: "Post a text message to a Slack incoming webhook, optionally setting the channel and username on the JSON payload."
# tags: [slack, communication]
# added: "2026-08-18T19:55:27+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs an incoming webhook URL. Requires LWP::UserAgent and JSON."
# end-snippet
use strict;
use warnings;

use HTTP::Request::Common qw(POST);
use LWP::UserAgent;
use JSON;

sub post_slack {
    my ($webhook_url, $channel, $username, $message) = @_;

    my $ua = LWP::UserAgent->new;
    $ua->timeout(15);

    my $json = encode_json({
        channel  => $channel,
        username => $username,
        text     => $message,
    });
    my $req  = POST($webhook_url, ['payload' => $json]);
    my $resp = $ua->request($req);
    die $resp->status_line unless $resp->is_success;
}
