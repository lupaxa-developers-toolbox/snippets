# snippet:
# title: Retry a block
# card_title: "Retry a block"
# summary: "Re-run a block with exponential backoff until it succeeds or hits a retry limit, sleeping longer after each failed attempt."
# tags: [retry]
# added: "2026-08-18T18:03:19+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: Not for blocks that are not idempotent.
# end-snippet

def retry_call(attempts: 5, delay: 1.0)
  current = delay
  tries = 0
  begin
    yield
  rescue StandardError
    tries += 1
    raise if tries >= attempts

    sleep current
    current *= 2
    retry
  end
end
