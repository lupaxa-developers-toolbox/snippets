// snippet:
// title: "Handle Uncaught Errors Safely"
// card_title: "Uncaught Error Handlers"
// summary: "Log unhandled promise rejections and uncaught exceptions so a process does not fail silently, then exit after an uncaught exception."
// tags: [process, errors]
// added: "2026-08-21T13:41:30+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Register these listeners at startup. After uncaughtException the process is in an unknown state, so this exits rather than continuing. unhandledRejection does not exit; add process.exit(1) there too if you want the same policy."
// end-snippet
process.on("unhandledRejection", (err) => {
  console.error("Unhandled rejection:", err);
});

process.on("uncaughtException", (err) => {
  console.error("Uncaught exception:", err);
  process.exit(1);
});
