/**
 * Open snippet cards in a dialog instead of navigating to the page.
 *
 * The built snippet page stays the source of highlighted code and caveats.
 */

(() => {
  "use strict";

  const { onPageRender } = window.LupaxaPageLifecycle;
  const DIALOG_SELECTOR = "[data-snippet-modal]";

  let fetchGeneration = 0;
  let savedScrollX = 0;
  let savedScrollY = 0;

  function rememberScroll() {
    savedScrollX = window.scrollX;
    savedScrollY = window.scrollY;
  }

  function restoreScroll() {
    window.scrollTo(savedScrollX, savedScrollY);
  }

  /**
   * @returns {HTMLDialogElement}
   */
  function ensureDialog() {
    const existing = document.querySelector(DIALOG_SELECTOR);

    if (existing instanceof HTMLDialogElement) {
      return existing;
    }

    const dialog = document.createElement("dialog");

    dialog.className = "snippet-modal";
    dialog.dataset.snippetModal = "";
    dialog.innerHTML = `
      <button
        type="button"
        class="snippet-modal__nav snippet-modal__nav--prev"
        data-snippet-modal-prev
        aria-label="Previous snippet"
        hidden
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M15.41 7.41 14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
        </svg>
      </button>
      <div class="snippet-modal__frame">
        <button
          type="button"
          class="snippet-modal__close"
          data-snippet-modal-close
          aria-label="Close"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        </button>
        <div class="snippet-modal__panel md-typeset">
          <div class="snippet-modal__body" data-snippet-modal-body></div>
        </div>
      </div>
      <button
        type="button"
        class="snippet-modal__nav snippet-modal__nav--next"
        data-snippet-modal-next
        aria-label="Next snippet"
        hidden
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M10 6 8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
        </svg>
      </button>
    `;

    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) {
        dialog.close();
        return;
      }

      const languageLink = event.target.closest(
        "[data-snippet-language-meta] a",
      );

      if (!(languageLink instanceof HTMLAnchorElement)) {
        return;
      }

      dialog.close();

      const languageSelect = document.querySelector(
        "[data-snippet-filters] [data-snippet-language]",
      );

      if (!(languageSelect instanceof HTMLSelectElement)) {
        return;
      }

      const language = new URL(
        languageLink.getAttribute("href") || "",
        window.location.origin,
      ).searchParams.get("language");

      if (
        !language ||
        ![...languageSelect.options].some((option) => option.value === language)
      ) {
        return;
      }

      event.preventDefault();
      languageSelect.value = language;
      languageSelect.dispatchEvent(new Event("change", { bubbles: true }));
    });

    dialog.addEventListener("close", () => {
      restoreScroll();
      requestAnimationFrame(restoreScroll);
    });

    dialog
      .querySelector("[data-snippet-modal-close]")
      ?.addEventListener("click", () => {
        dialog.close();
      });

    dialog
      .querySelector("[data-snippet-modal-prev]")
      ?.addEventListener("click", () => {
        navigateModal(dialog, -1);
      });

    dialog
      .querySelector("[data-snippet-modal-next]")
      ?.addEventListener("click", () => {
        navigateModal(dialog, 1);
      });

    dialog.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        navigateModal(dialog, -1);
      } else if (event.key === "ArrowRight") {
        event.preventDefault();
        navigateModal(dialog, 1);
      }
    });

    document.body.append(dialog);

    return dialog;
  }

  function closeDialog() {
    fetchGeneration += 1;

    const dialog = document.querySelector(DIALOG_SELECTOR);

    if (dialog instanceof HTMLDialogElement && dialog.open) {
      dialog.close();
    }
  }

  /**
   * Visible snippet cards in current catalogue order (filters + sort).
   *
   * @returns {HTMLAnchorElement[]}
   */
  function visibleSnippetLinks() {
    const links = [];

    document
      .querySelectorAll(
        ".catalogue-grid:not(.catalogue-grid--languages) a[data-snippet-card]",
      )
      .forEach((node) => {
        if (!(node instanceof HTMLAnchorElement) || !node.href) {
          return;
        }

        const card = node.closest("li");

        if (card?.hidden) {
          return;
        }

        links.push(node);
      });

    return links;
  }

  /**
   * @param {string} left
   * @param {string} right
   * @returns {boolean}
   */
  function sameSnippetHref(left, right) {
    try {
      return new URL(left, window.location.href).pathname
        === new URL(right, window.location.href).pathname;
    } catch {
      return left === right;
    }
  }

  /**
   * @param {HTMLDialogElement} dialog
   */
  function syncNavButtons(dialog) {
    const prev = dialog.querySelector("[data-snippet-modal-prev]");
    const next = dialog.querySelector("[data-snippet-modal-next]");
    const cards = visibleSnippetLinks();
    const show = cards.length > 1;

    if (prev instanceof HTMLButtonElement) {
      prev.hidden = !show;
    }

    if (next instanceof HTMLButtonElement) {
      next.hidden = !show;
    }

    dialog.classList.toggle("snippet-modal--loop", show);
  }

  /**
   * @param {HTMLDialogElement} dialog
   * @param {number} offset
   */
  function navigateModal(dialog, offset) {
    const cards = visibleSnippetLinks();

    if (cards.length < 2) {
      return;
    }

    const current = dialog.dataset.snippetHref || "";
    const index = cards.findIndex((link) => sameSnippetHref(link.href, current));

    if (index < 0) {
      return;
    }

    const target = cards[(index + offset + cards.length) % cards.length];
    const title =
      target.dataset.fullTitle?.trim() || target.textContent?.trim() || "";

    void openSnippetModal(target.href, title);
  }

  /**
   * @param {ParentNode} root
   */
  function stripFragmentLinks(root) {
    root.querySelectorAll("[id]").forEach((node) => {
      node.removeAttribute("id");
    });
    root.querySelectorAll('a[href^="#"]').forEach((node) => {
      node.replaceWith(...node.childNodes);
    });
  }

  /**
   * @param {HTMLElement} highlight
   */
  function attachClipboard(highlight) {
    const code = highlight.querySelector("pre code, pre");

    if (!code) {
      return;
    }

    const button = document.createElement("button");

    button.type = "button";
    button.className = "md-clipboard md-icon";
    button.title = "Copy to clipboard";
    button.setAttribute("aria-label", "Copy to clipboard");

    button.addEventListener("click", async () => {
      const text = code.textContent ?? "";

      try {
        await navigator.clipboard.writeText(text);
        button.dataset.copied = "true";
        button.title = "Copied";
        button.setAttribute("aria-label", "Copied");
      } catch {
        button.title = "Copy failed";
      }

      window.setTimeout(() => {
        delete button.dataset.copied;
        button.title = "Copy to clipboard";
        button.setAttribute("aria-label", "Copy to clipboard");
      }, 1600);
    });

    highlight.append(button);
  }

  /**
   * @param {HTMLElement} body
   * @param {string} message
   */
  function showModalError(body, message) {
    body.innerHTML = `<p class="snippet-modal-status">${message}</p>`;
  }

  /**
   * @param {string} href
   * @param {string} title
   */
  async function openSnippetModal(href, title) {
    const dialog = ensureDialog();
    const body = dialog.querySelector("[data-snippet-modal-body]");

    if (!(body instanceof HTMLElement)) {
      return;
    }

    const generation = (fetchGeneration += 1);
    const alreadyOpen = dialog.open;

    dialog.setAttribute("aria-label", title || "Snippet");
    dialog.dataset.snippetHref = href;
    body.innerHTML = '<p class="snippet-modal-status">Loading snippet…</p>';
    syncNavButtons(dialog);

    if (!alreadyOpen) {
      rememberScroll();
      dialog.showModal();
      restoreScroll();
      requestAnimationFrame(restoreScroll);
    }

    let response;

    try {
      response = await fetch(href, { headers: { Accept: "text/html" } });
    } catch {
      if (generation === fetchGeneration) {
        showModalError(body, "Could not load this snippet.");
      }

      return;
    }

    if (generation !== fetchGeneration) {
      return;
    }

    if (!response.ok) {
      showModalError(body, "Could not load this snippet.");
      return;
    }

    const html = await response.text();

    if (generation !== fetchGeneration) {
      return;
    }

    const parsed = new DOMParser().parseFromString(html, "text/html");
    const article = parsed.querySelector("[data-snippet-article]");

    if (!article) {
      showModalError(body, "Could not load this snippet.");
      return;
    }

    const pageTitle =
      parsed.querySelector("article h1")?.textContent?.trim() || title;
    const meta = article.querySelector("[data-snippet-meta]");
    const date = article.querySelector("[data-snippet-added]");
    const submitted = article.querySelector("[data-snippet-submitted]");
    const highlight = article.querySelector(".highlight");
    const caveats = article.querySelector(".admonition");

    body.replaceChildren();

    if (pageTitle) {
      const heading = document.createElement("h2");

      heading.className = "snippet-modal-title";
      heading.id = "snippet-modal-title";
      heading.textContent = pageTitle;
      body.append(heading);
      dialog.setAttribute("aria-labelledby", heading.id);
    }

    if (meta instanceof HTMLElement) {
      const metaNode = meta.cloneNode(true);

      if (metaNode instanceof HTMLElement) {
        stripFragmentLinks(metaNode);
        body.append(metaNode);
      }
    } else if (date) {
      const dateNode = date.cloneNode(true);

      if (dateNode instanceof HTMLElement) {
        stripFragmentLinks(dateNode);

        const dateText = dateNode.textContent?.trim() || "";

        if (dateText && !dateText.toLowerCase().startsWith("added on")) {
          dateNode.innerHTML = `Added on: ${dateNode.innerHTML.trim()}`;
        }

        body.append(dateNode);
      }

      if (submitted instanceof HTMLElement) {
        const submittedNode = submitted.cloneNode(true);

        if (submittedNode instanceof HTMLElement) {
          stripFragmentLinks(submittedNode);
          body.append(submittedNode);
        }
      }
    }

    if (highlight) {
      const codeNode = highlight.cloneNode(true);

      if (codeNode instanceof HTMLElement) {
        stripFragmentLinks(codeNode);
        attachClipboard(codeNode);
        body.append(codeNode);
      }
    }

    if (caveats) {
      const caveatsNode = caveats.cloneNode(true);

      if (caveatsNode instanceof HTMLElement) {
        stripFragmentLinks(caveatsNode);
        body.append(caveatsNode);
      }
    }
  }

  document.addEventListener(
    "click",
    (event) => {
      if (!(event.target instanceof Element)) {
        return;
      }

      if (
        event.target.closest(
          ".catalogue-category, [data-language-filter-control], .catalogue-grid p:has(img.catalogue-logo)",
        )
      ) {
        return;
      }

      const card = event.target.closest(
        ".catalogue-grid:not(.catalogue-grid--languages) > ul > li, .catalogue-grid:not(.catalogue-grid--languages) > li",
      );

      if (!card) {
        return;
      }

      const link = card.querySelector("a[data-snippet-card]");

      if (!(link instanceof HTMLAnchorElement) || !link.href) {
        return;
      }

      event.preventDefault();
      event.stopImmediatePropagation();

      const title = link.textContent?.trim() || "";

      void openSnippetModal(link.href, title);
    },
    true,
  );

  onPageRender(closeDialog);
})();
