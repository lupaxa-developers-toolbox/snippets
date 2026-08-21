// snippet:
// title: "Simple logger middleware pattern"
// card_title: "Logger middleware"
// summary: "Wrap a Node.js request handler so each response logs method, URL, status, and elapsed milliseconds when the response finishes."
// tags: [http, logging]
// added: "2026-08-21T13:41:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Framework-free: pass this wrapper to http.createServer. Logs on the finish event, so early socket drops may not appear. statusCode is 200 until the handler sets another."
// end-snippet
function withLogging(handler) {
  return (req, res) => {
    const start = Date.now();
    res.on("finish", () => {
      console.log(req.method, req.url, res.statusCode, `${Date.now() - start}ms`);
    });
    handler(req, res);
  };
}
