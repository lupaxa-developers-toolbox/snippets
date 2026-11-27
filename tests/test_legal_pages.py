"""Sponsor widget, legal footer, and analytics opt-out."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MKDOCS_YML = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
SPONSOR_MD = (ROOT / "mkdocs/sponsor.md").read_text(encoding="utf-8")
FOOTER = (ROOT / "overrides/partials/footer.html").read_text(encoding="utf-8")
MAIN = (ROOT / "overrides/main.html").read_text(encoding="utf-8")
LEGAL = ROOT / "mkdocs" / "legal"


def test_sponsor_widget_waits_for_a_click() -> None:
    assert ('data-src="https://ko-fi.com/thelupaxaproject/?hidefeed=true&widget=true&embed=true"') in SPONSOR_MD
    assert ' src="' not in SPONSOR_MD
    assert "sponsor-widget-open" in SPONSOR_MD
    assert "Open Ko-fi Widget" in SPONSOR_MD
    assert "Open our Ko-fi Page" in SPONSOR_MD
    assert "assets/javascript/sponsor.js" in MKDOCS_YML


def test_footer_links_the_four_policies() -> None:
    assert "href=\"{{ 'legal/privacy-policy/' | url }}\"" in FOOTER
    assert "href=\"{{ 'legal/website-terms/' | url }}\"" in FOOTER
    assert "href=\"{{ 'legal/copyright-and-licensing/' | url }}\"" in FOOTER
    assert "href=\"{{ 'legal/disclaimer/' | url }}\"" in FOOTER
    assert "footer-home-link" in FOOTER


def test_analytics_skip_a_browser_that_opted_out() -> None:
    assert 'localStorage.getItem("lupaxa-counter") === "off"' in MAIN
    assert 'localStorage.getItem("lupaxa-cloudflare") === "off"' in MAIN
    assert "config.extra.cloudflare_analytics_token" in MAIN
    assert "cloudflare_analytics_token: 3b693af588994e60aaed7feebcd9d41a" in MKDOCS_YML
    assert "assets/javascript/counter-choice.js" in MKDOCS_YML


def test_policies_describe_this_site() -> None:
    pages = {
        "privacy-policy.md": "snippets.thelupaxaproject.org",
        "website-terms.md": "particular snippet",
        "copyright-and-licensing.md": "lupaxa-developers-toolbox/snippets",
        "disclaimer.md": "code in a snippet",
    }
    for name, marker in pages.items():
        text = (LEGAL / name).read_text(encoding="utf-8")
        assert marker in text
        assert "humour" not in text.lower()
        assert "catalogue of projects" not in text.lower()
    privacy = (LEGAL / "privacy-policy.md").read_text(encoding="utf-8")
    assert 'data-analytics-key="lupaxa-counter"' in privacy
    assert 'data-analytics-key="lupaxa-cloudflare"' in privacy
