# snippet:
# title: "Forked workers with a timeout"
# card_title: "Forked workers timeout"
# summary: "Run Parallel::ForkManager jobs and kill any child whose runtime exceeds PATIENCE seconds so hung workers cannot stall the pool."
# tags: [concurrency, timeout]
# added: "2026-08-18T19:55:28+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs Parallel::ForkManager. Adjust PATIENCE, max threads, and the work function."
# end-snippet
use strict;
use warnings;

use Parallel::ForkManager;

use constant PATIENCE => 3;

our %workers;
our %threads;

my $max_threads   = 15;
my $total_threads = 100;

sub actually_do_something {
    my ($c) = @_;
    print "Thread number: $c\n";
    sleep 5;
}

sub dismiss_hung_workers {
    while (my ($pid, $started_at) = each %workers) {
        next unless time() - $started_at > PATIENCE;
        print "Timeout for thread $threads{$pid} (PID $pid)\n";
        kill TERM => $pid;
        delete $threads{$pid};
        delete $workers{$pid};
    }
}

sub main {
    my $pm = Parallel::ForkManager->new($max_threads);

    $pm->run_on_wait(\&dismiss_hung_workers, 1);

    for my $i (0 .. $total_threads) {
        if (my $pid = $pm->start) {
            $threads{$pid} = $i;
            $workers{$pid} = time();
            next;
        }
        actually_do_something($i);
        $pm->finish;
    }
    $pm->wait_all_children;
}
