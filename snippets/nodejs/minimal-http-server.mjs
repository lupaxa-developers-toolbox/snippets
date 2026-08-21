// snippet:
// title: "Minimal HTTP server with routing"
// card_title: "Minimal HTTP router"
// summary: "Start a Node.js HTTP server with no framework: exact-path routes for / and /health, and a 404 for everything else."
// tags: [http, server]
// added: "2026-08-21T13:38:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "ES module: run as .mjs, or set type module in package.json. Listens on port 3000. req.url includes the query string, so /health?ready=1 is 404."
// end-snippet
import http from "node:http";

http.createServer((req, res) => {
  if (req.url === "/") {
    return res.end("Home");
  }
  if (req.url === "/health") {
    return res.end("OK");
  }
  res.writeHead(404);
  res.end("Not Found");
}).listen(3000);
