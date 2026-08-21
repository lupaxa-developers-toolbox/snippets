// snippet:
// title: "Prompt the user in the terminal"
// card_title: "Terminal prompt"
// summary: "Ask a question on stdin with node:readline, wait for the answer as a promise, then close the interface."
// tags: [cli, readline]
// added: "2026-08-21T13:42:30+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "ES module with top-level await: run as .mjs, or set type module in package.json. Needs a TTY. Empty input is an empty string, not null."
// end-snippet
import readline from "node:readline";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const answer = await new Promise((resolve) => {
  rl.question("Your name? ", resolve);
});
rl.close();

console.log(`Hello ${answer}`);
