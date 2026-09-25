<p align="center">
  <a href="https://github.com/lupaxa-developers-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/developers-toolbox/readme-logo.png" alt="Developers Toolbox" />
  </a>
</p>

<h1 align="center">Snippets</h1>

A curated collection of reusable code snippets for Shell, Python, Ruby, and
other languages. Browse by language or tag, open a snippet in place, and copy
highlighted examples with caveats when they matter.

## Add a Snippet

Put a file at `snippets/<language>/<slug>.<ext>` with a `snippet:` /
`end-snippet` comment fence. Required fields are `title` (modal heading),
`card_title` (catalogue card, at most 28 characters), `summary`, `tags`,
`added` (ISO-8601), and `submitted_by` (GitHub userid). Optional fields are
`runnable` and `caveats`.

```bash
# snippet:
# title: Retry a Command
# card_title: Retry a Command
# summary: Re-run a command with exponential backoff until it succeeds or hits a retry limit.
# tags: [retry]
# added: "2026-08-18T18:03:18+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: Not for commands that are not idempotent.
# end-snippet
```

Use `#` for shell and Python, `//` for C-family languages, or `--` for SQL.
Rebuild or refresh the MkDocs preview to see the card on Home and Snippets.

## Documentation

Site pages live in `mkdocs/` and publish to
<https://snippets.thelupaxaproject.org/>.

```bash
make init
make python-install-dev
make mkdocs-serve
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
