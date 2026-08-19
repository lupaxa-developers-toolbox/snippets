# snippet:
# title: "Keep the smaller or larger value"
# card_title: "Keep min or max"
# summary: "Return the smaller or larger of two comparable values so callers can keep a running minimum or maximum without writing the comparison themselves."
# tags: [math]
# added: "2026-08-18T19:55:31+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
def keep_min(left, right)
  (left <=> right) <= 0 ? left : right
end

def keep_max(left, right)
  (left <=> right) >= 0 ? left : right
end
