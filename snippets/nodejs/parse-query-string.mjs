// snippet:
// title: "Parse query string parameters"
// card_title: "Parse query string"
// summary: "Read query parameters from an incoming request with WHATWG URL and searchParams, using a fallback when the key is missing."
// tags: [http, query]
// added: "2026-08-21T13:40:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "ES module: run as .mjs, or set type module in package.json. Listens on port 3000. The http://localhost base is only for parsing; it is not the listen address. searchParams.get returns the first value only."
// end-snippet
import http from "node:http";
import { URL } from "node:url";

http.createServer((req, res) => {
  const url = new URL(req.url, "http://localhost");
  const name = url.searchParams.get("name") ?? "friend";
  res.end(`Hi ${name}`);
}).listen(3000);
