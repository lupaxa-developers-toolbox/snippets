# snippet:
# title: "Simple ForkManager worker pool"
# card_title: "ForkManager worker pool"
# summary: "Fork a fixed-size Parallel::ForkManager worker pool, start each job in a child process, and wait until every worker has finished."
# tags: [concurrency]
# added: "2026-08-18T19:55:26+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: "Needs Parallel::ForkManager."
# end-snippet
use Parallel::ForkManager;

my $max_threads   = 5;
my $total_threads = 25;

my $pm = Parallel::ForkManager->new($max_threads);

sub actually_do_something {
    my ($c) = @_;
    print "Thread number: $c\n";
    sleep 5;
}

for my $i (0 .. $total_threads) {
    my $pid = $pm->start and next;
    actually_do_something($i);
    $pm->finish;
}

$pm->wait_all_children;
