from pathlib import Path

from snippets_mkdocs.scan import scan_snippets


def test_seed_snippets_scan() -> None:
    root = Path(__file__).resolve().parents[1] / "snippets"
    snippets = scan_snippets(root)
    keys = {(item.language, item.slug) for item in snippets}
    assert {
        ("perl", "slack"),
        ("php", "array-key-search"),
        ("python", "retry"),
        ("ruby", "keep"),
        ("ruby", "retry"),
        ("shell", "pause"),
        ("shell", "get-confirmation"),
    } <= keys
    assert ("shell", "confirm") not in keys
    assert ("shell", "retry") not in keys
    assert ("shell", "run-cmd") not in keys
    assert ("ruby", "keep-min") not in keys
    assert ("ruby", "keep-max") not in keys
    by_key = {(item.language, item.slug): item for item in snippets}
    for language in ("python", "ruby"):
        retry = by_key[(language, "retry")]
        assert retry.tags == ("retry",)
        assert retry.runnable is False
    assert by_key[("shell", "pause")].tags == ("interactive",)
    assert by_key[("shell", "get-confirmation")].tags == ("interactive",)
    assert by_key[("perl", "slack")].tags == ("slack", "communication")
    assert by_key[("ruby", "keep")].tags == ("math",)
