# snippet:
# title: "Fork pool with hung cleanup"
# card_title: "Fork pool hang cleanup"
# summary: "Track worker PIDs and thread IDs in a Parallel::ForkManager pool, then kill children that exceed PATIENCE so hung jobs are cleaned up."
# tags: [concurrency, timeout]
# added: "2026-08-18T19:55:25+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs Parallel::ForkManager."
# end-snippet
use strict;
use warnings;

use Parallel::ForkManager;

use constant PATIENCE => 50;

my %workers = ();
my %tids    = ();
my %pids    = ();

my $max_forks   = 3;
my $total_forks = 10;

sub actually_do_something {
    my ($c) = @_;
    print "Fork ID number: $c\n";
    sleep 3;
}

sub cleanup_by_pid {
    my ($pid) = @_;
    my $tid = $pids{$pid};
    delete $tids{$tid} if defined $tid;
    delete $pids{$pid};
    delete $workers{$pid};
}

sub cleanup_by_threadid {
    my ($tid) = @_;
    my $pid = $tids{$tid};
    delete $tids{$tid};
    delete $pids{$pid} if defined $pid;
    delete $workers{$pid} if defined $pid;
}

sub dismiss_hung_workers {
    while (my ($pid, $started_at) = each %workers) {
        next unless time() - $started_at > PATIENCE;
        kill TERM => $pid;
        cleanup_by_pid($pid);
    }
}

sub main {
    my $pm = Parallel::ForkManager->new($max_forks);

    $pm->run_on_wait(\&dismiss_hung_workers, 1);
    $pm->run_on_finish(sub {
        my ($pid, $tid) = @_;
        cleanup_by_threadid($tid);
    });

    for my $i (1 .. $total_forks) {
        if (my $pid = $pm->start) {
            $tids{$i}      = $pid;
            $pids{$pid}    = $i;
            $workers{$pid} = time();
            next;
        }
        actually_do_something($i);
        $pm->finish($i);
    }
    $pm->wait_all_children;
}
