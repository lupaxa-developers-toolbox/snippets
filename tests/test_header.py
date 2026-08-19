import pytest

from snippets_mkdocs.errors import SnippetError
from snippets_mkdocs.header import parse_header

BASH = """# snippet:
# title: Retry a command
# card_title: Retry a command
# summary: Re-run a command with backoff.
# tags: [process, retry]
# added: "2026-08-18T18:03:18+01:00"
# submitted_by: Lupraxus
# runnable: false
# caveats: Not for commands that are not idempotent.
# end-snippet

retry() { :; }
"""

SLASH = """// snippet:
// title: Hello
// card_title: Hello
// summary: A tiny example.
// tags: [demo]
// added: "2026-01-01T00:00:00+00:00"
// submitted_by: Lupraxus
// end-snippet

export const hello = 1;
"""

DASH = """-- snippet:
-- title: Hello
-- card_title: Hello
-- summary: A tiny example.
-- tags: [demo]
-- added: "2026-01-01T00:00:00+00:00"
-- submitted_by: Lupraxus
-- end-snippet

SELECT 1;
"""


def test_parse_hash_header_and_strip_body() -> None:
    meta, body = parse_header(BASH, path="snippets/shell/retry.sh")
    assert meta.title == "Retry a command"
    assert meta.card_title == "Retry a command"
    assert meta.summary == "Re-run a command with backoff."
    assert meta.tags == ("process", "retry")
    assert meta.added.isoformat() == "2026-08-18T18:03:18+01:00"
    assert meta.submitted_by == "Lupraxus"
    assert meta.runnable is False
    assert meta.caveats == "Not for commands that are not idempotent."
    assert body == "retry() { :; }\n"


def test_parse_slash_and_dash_comments() -> None:
    meta, _ = parse_header(SLASH, path="a.js")
    assert meta.title == "Hello"
    assert meta.card_title == "Hello"
    meta, _ = parse_header(DASH, path="a.sql")
    assert meta.title == "Hello"
    assert meta.card_title == "Hello"


def test_runnable_defaults_false() -> None:
    text = """# snippet:
# title: T
# card_title: T
# summary: S
# tags: [demo]
# added: "2026-01-01T00:00:00+00:00"
# submitted_by: Lupraxus
# end-snippet

x
"""
    meta, _ = parse_header(text)
    assert meta.runnable is False
    assert meta.submitted_by == "Lupraxus"
    assert meta.added.year == 2026
    assert meta.caveats is None


def test_missing_fence_raises() -> None:
    with pytest.raises(SnippetError) as exc:
        parse_header("echo hi\n", path="snippets/shell/hi.sh")
    assert exc.value.path == "snippets/shell/hi.sh"


def test_missing_title_names_field() -> None:
    text = """# snippet:
# summary: S
# tags: [demo]
# end-snippet

x
"""
    with pytest.raises(SnippetError) as exc:
        parse_header(text, path="f.sh")
    assert exc.value.field == "title"


def test_missing_card_title_names_field() -> None:
    text = """# snippet:
# title: T
# summary: S
# tags: [demo]
# end-snippet

x
"""
    with pytest.raises(SnippetError) as exc:
        parse_header(text, path="f.sh")
    assert exc.value.field == "card_title"


def test_card_title_too_long_raises() -> None:
    text = """# snippet:
# title: A longer modal heading
# card_title: This card title is far too long to fit
# summary: S
# tags: [demo]
# added: "2026-01-01T00:00:00+00:00"
# submitted_by: Lupraxus
# end-snippet

x
"""
    with pytest.raises(SnippetError) as exc:
        parse_header(text, path="f.sh")
    assert exc.value.field == "card_title"


def test_bad_tag_token_raises() -> None:
    text = """# snippet:
# title: T
# card_title: T
# summary: S
# tags: [Retry]
# end-snippet

x
"""
    with pytest.raises(SnippetError) as exc:
        parse_header(text, path="f.sh")
    assert exc.value.field == "tags"


def test_mixed_comment_prefix_raises() -> None:
    text = """# snippet:
# title: T
# card_title: T
# summary: S
# tags: [demo]
// end-snippet

x
"""
    with pytest.raises(SnippetError) as exc:
        parse_header(text, path="f.sh")
    assert "inconsistent comment prefix" in str(exc.value)


def test_missing_added_raises() -> None:
    text = """# snippet:
# title: T
# card_title: T
# summary: S
# tags: [demo]
# end-snippet

x
"""
    with pytest.raises(SnippetError) as exc:
        parse_header(text, path="f.sh")
    assert exc.value.field == "added"


def test_missing_submitted_by_raises() -> None:
    text = """# snippet:
# title: T
# card_title: T
# summary: S
# tags: [demo]
# added: "2026-01-01T00:00:00+00:00"
# end-snippet

x
"""
    with pytest.raises(SnippetError) as exc:
        parse_header(text, path="f.sh")
    assert exc.value.field == "submitted_by"


def test_bad_submitted_by_raises() -> None:
    text = """# snippet:
# title: T
# card_title: T
# summary: S
# tags: [demo]
# added: "2026-01-01T00:00:00+00:00"
# submitted_by: not a user
# end-snippet

x
"""
    with pytest.raises(SnippetError) as exc:
        parse_header(text, path="f.sh")
    assert exc.value.field == "submitted_by"


def test_empty_tags_raises() -> None:
    text = """# snippet:
# title: T
# card_title: T
# summary: S
# tags: []
# end-snippet

x
"""
    with pytest.raises(SnippetError) as exc:
        parse_header(text)
    assert exc.value.field == "tags"
