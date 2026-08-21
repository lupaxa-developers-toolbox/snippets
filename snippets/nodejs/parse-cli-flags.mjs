// snippet:
// title: "Create a simple CLI argument parser"
// card_title: "Simple CLI flag parser"
// summary: "Turn process.argv flags of the form --key=value into an object, treating a bare --key as true."
// tags: [cli]
// added: "2026-08-21T13:42:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Only handles --key and --key=value. No short flags, quoting, or repeated keys (later values overwrite). Positional arguments become keys too."
// end-snippet
const args = process.argv.slice(2);
const flags = Object.fromEntries(args.map((a) => {
  const [k, v = "true"] = a.replace(/^--/, "").split("=");
  return [k, v];
}));

console.log(flags);
