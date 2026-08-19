# snippet:
# title: "Seconds to HH:MM:SS"
# card_title: "Seconds to HH:MM:SS"
# summary: "Format an integer number of seconds as a zero-padded HH:MM:SS clock string, including hours beyond 24 when the duration is long."
# tags: [time]
# added: "2026-08-18T19:55:33+01:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet
def seconds_to_hms(sec)
  [sec / 3600, sec / 60 % 60, sec % 60].map { |t| t.to_s.rjust(2, '0') }.join(':')
end
