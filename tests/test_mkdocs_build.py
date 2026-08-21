import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_mkdocs_build_strict() -> None:
    result = subprocess.run(
        ["python", "-m", "mkdocs", "build", "--strict"],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr + result.stdout


def _header_link(html: str, title: str) -> re.Match[str]:
    match = re.search(
        rf'class="lupaxa-header__nav-link"\s+href="([^"]+)"\s+'
        rf'data-nav-prefixes="([^"]*)"[^>]*>\s*{re.escape(title)}\s*<',
        html,
    )
    assert match is not None, f"missing header link {title}"
    return match


def test_built_snippets_page_has_filter_panel() -> None:
    test_mkdocs_build_strict()
    listing = (REPO / "site" / "snippets" / "index.html").read_text(encoding="utf-8")
    assert "data-snippet-filters" in listing
    assert "data-snippet-search" in listing
    assert "data-snippet-language" in listing
    assert "data-snippet-tag" in listing
    assert 'data-snippet-sort="alpha"' in listing
    assert 'data-snippet-sort="newest"' in listing
    assert "data-added=" in listing
    assert 'title="Shell"' in listing
    assert "data-snippet-catalogue" in listing
    assert "catalogue-filters.js" in listing
    assert "snippet-modal.js" in listing
    assert "data-snippet-card" in listing
    assert 'href="../shell/' in listing
    assert ".md" not in listing.split("data-snippet-card")[0][-40:]
    assert "filter-panel.css" in listing
    assert "<title>Catalogue - Snippets</title>" in listing
    assert 'id="listed-languages"' in listing
    listed = listing.split('id="listed-languages"')[1].split("</template>")[0]
    assert '"php"' in listed
    assert '"sql"' in listed
    assert '"nodejs"' in listed
    assert '"rust"' in listed
    assert '"kotlin"' not in listed
    assert 'value="php">PHP</option>' in listing
    assert 'value="sql">SQL</option>' in listing
    assert 'value="nodejs">Node.js</option>' in listing
    assert 'value="rust">Rust</option>' in listing
    assert 'value="kotlin"' not in listing


def test_built_header_and_body_chrome() -> None:
    test_mkdocs_build_strict()
    home = (REPO / "site" / "index.html").read_text(encoding="utf-8")
    pause = (REPO / "site" / "shell" / "pause" / "index.html").read_text(encoding="utf-8")
    assert "md-sidebar--primary" in home
    assert "lupaxa-header__drawer-button" in home
    assert "md-sidebar--secondary" not in home
    assert 'data-md-component="search"' not in home
    assert "lupaxa-header__search-button" not in home
    assert "Switch to light mode" not in home
    assert "Switch to dark mode" not in home
    assert 'data-md-color-scheme="slate"' in home
    snippets_home = _header_link(home, "Snippets")
    assert snippets_home.group(1) == "snippets/"
    assert "snippets/" in snippets_home.group(2).split()
    assert "shell/" in snippets_home.group(2).split()
    assert "python/retry/" not in snippets_home.group(2)
    primary_nav = home.split('class="md-nav md-nav--primary"', 1)[1].split("</nav>", 1)[0]
    assert "python/retry" not in primary_nav
    assert "shell/retry" not in primary_nav
    assert "data-snippet-card" in home
    assert "title=" in home
    languages_home = _header_link(home, "Languages")
    assert languages_home.group(1) == "languages/"
    assert not re.search(
        r'class="lupaxa-header__nav-link"[^>]*>\s*Tags\s*<',
        home,
    )
    snippets_pause = _header_link(pause, "Snippets")
    assert snippets_pause.group(1) == "../../snippets/"
    assert "data-snippet-article" in pause
    assert "data-snippet-language-meta" in pause
    assert 'Language: <a href="/snippets/?language=shell">Shell</a>' in pause
    assert "data-snippet-added" in pause
    assert "data-snippet-submitted" in pause
    assert "Submitted by:" in pause
    assert 'href="https://github.com/Lupraxus"' in pause
    assert "admonition" in pause
    languages_pause = _header_link(pause, "Languages")
    assert languages_pause.group(1) == "../../languages/"
    assert re.search(
        r"lupaxa-header__nav-item--active[\s\S]*?>\s*Snippets\s*<",
        pause,
    )
    languages_page = (REPO / "site" / "languages" / "index.html").read_text(encoding="utf-8")
    assert 'href="../snippets/?language=shell"' in languages_page
    assert 'href="../snippets/?language=php"' in languages_page
    assert 'href="../snippets/?language=sql"' in languages_page
    assert 'href="../snippets/?language=nodejs"' in languages_page
    assert 'href="../snippets/?language=rust"' in languages_page
    assert 'href="../snippets/?language=markdown"' not in languages_page
    assert 'src="../assets/images/languages/shell.png"' in languages_page
    assert 'src="../assets/images/languages/php.png"' in languages_page
    assert 'title="Shell"' not in languages_page
    assert 'title="PHP"' not in languages_page
    assert re.search(
        r"lupaxa-header__nav-item--active[\s\S]*?>\s*Languages\s*<",
        languages_page,
    )
    assert "?language=kotlin" not in languages_page
    assert "?language=swift" not in languages_page
    assert "?language=bash" not in languages_page
    assert "bash.png" not in languages_page
