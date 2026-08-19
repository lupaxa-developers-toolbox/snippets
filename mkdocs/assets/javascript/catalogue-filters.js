/**
 * Searchable catalogue filters for the Snippets page.
 *
 * Ported from thelupaxaproject.org/projects/ catalogue-filters.js
 * (language + tag instead of organisation + category).
 */

(() => {
  "use strict";

  const { onPageRender } = window.LupaxaPageLifecycle;

  const URL_PARAM_SEARCH = "search";
  const URL_PARAM_LANGUAGE = "language";
  const URL_PARAM_TAG = "tag";
  const URL_PARAM_SORT = "sort";
  const SORT_NEWEST = "newest";
  const SORT_ALPHA = "alpha";
  const CATALOGUE_LOCALE = "en-GB";

  /**
   * Whether the current URL already carries a catalogue filter.
   *
   * @returns {boolean}
   */
  function urlHasFilterParams() {
    const params = new URLSearchParams(window.location.search);

    return (
      params.has(URL_PARAM_SEARCH) ||
      params.has(URL_PARAM_LANGUAGE) ||
      params.has(URL_PARAM_TAG) ||
      params.has(URL_PARAM_SORT)
    );
  }

  /**
   * Expand or collapse a catalogue filter panel and keep the toggle in sync.
   *
   * @param {HTMLElement} filterPanel
   * @param {boolean} expanded
   */
  function setFilterPanelExpanded(filterPanel, expanded) {
    const button = filterPanel.querySelector("[data-filter-expand]");

    filterPanel.classList.toggle("filter-panel--expanded", expanded);

    if (!(button instanceof HTMLButtonElement)) {
      return;
    }

    button.setAttribute("aria-expanded", expanded ? "true" : "false");

    const label = button.querySelector(".filter-panel-expand__label");
    const labelText = expanded ? "Hide Filters" : "Show Filters";

    if (label) {
      label.textContent = labelText;
    } else {
      button.textContent = labelText;
    }
  }

  /**
   * Show the filter controls after a card pill or language mark applies a
   * filter, so the active selection is visible.
   *
   * @param {HTMLElement} filterPanel
   */
  function revealFilterPanel(filterPanel) {
    setFilterPanelExpanded(filterPanel, true);
    filterPanel.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
    });
  }

  /**
   * Collapsible filter toolbar.
   *
   * Panels start collapsed (Filters + summary only). Expand when the
   * button is pressed, when the URL already carries filter parameters,
   * or when a card control applies a filter.
   *
   * @param {HTMLElement} filterPanel
   */
  function initialiseFilterCollapse(filterPanel) {
    const button = filterPanel.querySelector("[data-filter-expand]");

    if (!(button instanceof HTMLButtonElement)) {
      return;
    }

    button.addEventListener("click", () => {
      filterPanel.dataset.collapseUserToggled = "true";
      setFilterPanelExpanded(
        filterPanel,
        !filterPanel.classList.contains("filter-panel--expanded"),
      );
    });

    setFilterPanelExpanded(filterPanel, urlHasFilterParams());
  }

  /**
   * Convert text into a consistent comparison value.
   *
   * @param {string} value
   * @returns {string}
   */
  function normaliseCatalogueValue(value) {
    return String(value ?? "")
      .toLocaleLowerCase(CATALOGUE_LOCALE)
      .replace(/\s+/g, " ")
      .trim();
  }

  /**
   * Display names from the generated catalogue JSON.
   *
   * @returns {Record<string, string>}
   */
  function languageLabelMap() {
    const node = document.getElementById("language-labels");

    if (!(node instanceof HTMLScriptElement) || !node.textContent) {
      return {};
    }

    try {
      const parsed = JSON.parse(node.textContent);
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch {
      return {};
    }
  }

  const LANGUAGE_LABELS = languageLabelMap();

  /**
   * Languages shown on the Languages page (visible or already have snippets).
   *
   * @returns {string[]}
   */
  function listedLanguageSlugs() {
    const node = document.getElementById("listed-languages");

    if (!(node instanceof HTMLScriptElement) || !node.textContent) {
      return [];
    }

    try {
      const parsed = JSON.parse(node.textContent);
      return Array.isArray(parsed) ? parsed.map(String) : [];
    } catch {
      return [];
    }
  }

  /**
   * Display name for a language folder slug.
   *
   * @param {string} value
   * @returns {string}
   */
  function languageLabel(value) {
    if (!value) {
      return value;
    }

    const mapped = LANGUAGE_LABELS[normaliseCatalogueValue(value)];

    if (mapped) {
      return mapped;
    }

    return value.charAt(0).toUpperCase() + value.slice(1);
  }

  /**
   * Add alphabetically sorted options to a select element.
   *
   * @param {HTMLSelectElement} select
   * @param {Map<string, string>} options
   */
  function addCatalogueOptions(select, options) {
    Array.from(options.entries())
      .sort((left, right) =>
        left[1].localeCompare(right[1], CATALOGUE_LOCALE),
      )
      .forEach(([value, label]) => {
        const option = document.createElement("option");

        option.value = value;
        option.textContent = label;

        select.append(option);
      });
  }

  /**
   * Return the tags attached to a catalogue card.
   *
   * @param {HTMLElement} card
   * @returns {{ values: string[], labels: string[] }}
   */
  function getCatalogueTags(card) {
    const labels = Array.from(card.querySelectorAll(".catalogue-category"))
      .map((tag) => tag.textContent?.trim() || "")
      .filter(Boolean);

    return {
      labels,
      values: labels.map(normaliseCatalogueValue),
    };
  }

  /**
   * Remove catalogue filter parameters from the current URL.
   */
  function clearCatalogueUrlParameters() {
    const url = new URL(window.location.href);

    url.searchParams.delete(URL_PARAM_SEARCH);
    url.searchParams.delete(URL_PARAM_LANGUAGE);
    url.searchParams.delete(URL_PARAM_TAG);

    window.history.replaceState(
      window.history.state,
      "",
      `${url.pathname}${url.search}${url.hash}`,
    );
  }

  /**
   * Remove temporary options created for URL-supplied filter values.
   *
   * @param {HTMLSelectElement} select
   */
  function removeUrlFilterOptions(select) {
    select.querySelectorAll("option[data-url-filter-option]").forEach((option) => {
      option.remove();
    });
  }

  /**
   * Initialise the snippets catalogue filters.
   */
  function initialiseCatalogue() {
    const filterPanel = document.querySelector("[data-snippet-filters]");
    const catalogue = document.querySelector("[data-snippet-catalogue]");

    if (!filterPanel || !catalogue) {
      return;
    }

    if (filterPanel.dataset.initialised === "true") {
      if (urlHasFilterParams()) {
        setFilterPanelExpanded(filterPanel, true);
      }

      return;
    }

    const searchInput = filterPanel.querySelector("[data-snippet-search]");
    const languageSelect = filterPanel.querySelector("[data-snippet-language]");
    const tagSelect = filterPanel.querySelector("[data-snippet-tag]");
    const clearButton = filterPanel.querySelector("[data-snippet-clear]");
    const summary = filterPanel.querySelector("[data-snippet-summary]");
    const emptyState = document.querySelector("[data-snippet-empty]");

    if (
      !searchInput ||
      !languageSelect ||
      !tagSelect ||
      !clearButton ||
      !summary
    ) {
      return;
    }

    filterPanel.dataset.initialised = "true";
    initialiseFilterCollapse(filterPanel);

    const cards = Array.from(catalogue.querySelectorAll(":scope > ul > li"));

    const tagOptions = new Map();
    const languageOptions = new Map();

    const cardData = cards.map((card) => {
      const tags = getCatalogueTags(card);
      const logo = card.querySelector(".catalogue-logo");
      const languageLabelText = logo?.dataset.language?.trim() || "";
      const languageValue = normaliseCatalogueValue(languageLabelText);

      tags.labels.forEach((label, index) => {
        tagOptions.set(tags.values[index], label);
      });

      if (languageValue) {
        languageOptions.set(
          languageValue,
          languageLabel(languageLabelText),
        );
      }

      const titleNode = card.querySelector(
        ":scope > p:first-child a[href], :scope > p:first-child strong",
      );

      return {
        element: card,
        tags: tags.values,
        language: languageValue,
        added: logo?.dataset.added?.trim() || "",
        title: (titleNode?.textContent || "").trim(),
        searchableText: normaliseCatalogueValue(
          [
            card.textContent || "",
            titleNode?.getAttribute("data-full-title") || "",
            languageLabelText,
            ...tags.labels,
          ].join(" "),
        ),
      };
    });

    listedLanguageSlugs().forEach((slug) => {
      const value = normaliseCatalogueValue(slug);

      if (value) {
        languageOptions.set(value, languageLabel(slug));
      }
    });

    addCatalogueOptions(tagSelect, tagOptions);
    addCatalogueOptions(languageSelect, languageOptions);

    const sortButtons = Array.from(
      filterPanel.querySelectorAll("[data-snippet-sort]"),
    );
    let activeSort = SORT_ALPHA;

    /**
     * @param {HTMLElement} button
     * @returns {string}
     */
    const sortFromButton = (button) =>
      String(button.dataset.snippetSort ?? "");

    /**
     * @returns {string}
     */
    const readSortFromUrl = () => {
      const value = new URLSearchParams(window.location.search).get(
        URL_PARAM_SORT,
      );

      return value === SORT_NEWEST ? SORT_NEWEST : SORT_ALPHA;
    };

    /**
     * @param {string} sort
     */
    const setSortPressed = (sort) => {
      sortButtons.forEach((button) => {
        button.setAttribute(
          "aria-pressed",
          sortFromButton(button) === sort ? "true" : "false",
        );
      });
    };

    /**
     * @param {Object} left
     * @param {Object} right
     * @returns {number}
     */
    const compareCards = (left, right) => {
      if (activeSort === SORT_NEWEST) {
        const leftDate = left.added || "";
        const rightDate = right.added || "";

        if (leftDate !== rightDate) {
          if (!leftDate) {
            return 1;
          }

          if (!rightDate) {
            return -1;
          }

          return rightDate.localeCompare(leftDate);
        }
      }

      return left.title.localeCompare(right.title, CATALOGUE_LOCALE, {
        sensitivity: "base",
      });
    };

    const applyCardOrder = () => {
      const list = catalogue.querySelector(":scope > ul");

      if (!list) {
        return;
      }

      const ordered = [...cardData].sort(compareCards);

      ordered.forEach((card) => {
        list.append(card.element);
      });

      cardData.length = 0;
      cardData.push(...ordered);
    };

    /**
     * Select a URL-supplied filter value.
     *
     * When the value does not exist among the generated options, add a
     * temporary option so that the requested filter remains active and the
     * catalogue correctly displays its empty state.
     *
     * @param {HTMLSelectElement} select
     * @param {string} value
     */
    const applySelectFilter = (select, value) => {
      const normalisedValue = normaliseCatalogueValue(value);

      const optionExists = Array.from(select.options).some(
        (option) => option.value === normalisedValue,
      );

      if (!optionExists) {
        const option = document.createElement("option");

        option.value = normalisedValue;
        option.textContent =
          select === languageSelect ? languageLabel(value) : value.trim();
        option.dataset.urlFilterOption = "";

        select.append(option);
      }

      select.value = normalisedValue;
    };

    /**
     * Populate available controls from the current URL.
     */
    const applyInitialFilters = () => {
      const urlParameters = new URLSearchParams(window.location.search);

      const search = urlParameters.get(URL_PARAM_SEARCH);
      const language = urlParameters.get(URL_PARAM_LANGUAGE);
      const tag = urlParameters.get(URL_PARAM_TAG);

      if (search !== null) {
        searchInput.value = search;
      }

      if (language !== null) {
        applySelectFilter(languageSelect, language);
      }

      if (tag !== null) {
        applySelectFilter(tagSelect, tag);
      }
    };

    /**
     * Read the current filter control values.
     *
     * @returns {{
     *   searchTerm: string,
     *   selectedLanguage: string,
     *   selectedTag: string
     * }}
     */
    const readActiveFilters = () => ({
      searchTerm: normaliseCatalogueValue(searchInput.value),
      selectedLanguage: normaliseCatalogueValue(languageSelect.value),
      selectedTag: normaliseCatalogueValue(tagSelect.value),
    });

    /**
     * Apply visibility to each card for the active filters.
     *
     * @param {{
     *   searchTerm: string,
     *   selectedLanguage: string,
     *   selectedTag: string
     * }} filters
     * @returns {number}
     */
    const applyCardVisibility = (filters) => {
      let visibleCount = 0;

      cardData.forEach((card) => {
        const matchesSearch =
          filters.searchTerm === "" ||
          card.searchableText.includes(filters.searchTerm);

        const matchesLanguage =
          filters.selectedLanguage === "" ||
          card.language === filters.selectedLanguage;

        const matchesTag =
          filters.selectedTag === "" ||
          card.tags.includes(filters.selectedTag);

        const isVisible = matchesSearch && matchesLanguage && matchesTag;

        card.element.hidden = !isVisible;

        if (isVisible) {
          visibleCount += 1;
        }
      });

      return visibleCount;
    };

    /**
     * Update the summary label for the current result set.
     *
     * @param {number} visibleCount
     */
    const updateSummary = (visibleCount) => {
      const totalCount = cardData.length;

      summary.textContent = `Showing ${visibleCount} of ${totalCount}`;
    };

    /**
     * Enable or disable the clear button from the active filters.
     *
     * @param {{
     *   searchTerm: string,
     *   selectedLanguage: string,
     *   selectedTag: string
     * }} filters
     */
    const updateClearButton = (filters) => {
      clearButton.disabled =
        filters.searchTerm === "" &&
        filters.selectedLanguage === "" &&
        filters.selectedTag === "";
    };

    /**
     * Show or hide the empty-state element.
     *
     * @param {number} visibleCount
     */
    const updateEmptyState = (visibleCount) => {
      if (emptyState) {
        emptyState.hidden = visibleCount !== 0;
      }
    };

    /**
     * Keep the URL synchronised with the current filters.
     *
     * @param {{
     *   searchTerm: string,
     *   selectedLanguage: string,
     *   selectedTag: string
     * }} filters
     */
    const syncUrlWithFilters = (filters) => {
      const params = new URLSearchParams();

      if (filters.searchTerm) {
        params.set(URL_PARAM_SEARCH, searchInput.value.trim());
      }

      if (filters.selectedLanguage) {
        params.set(URL_PARAM_LANGUAGE, languageSelect.value);
      }

      if (filters.selectedTag) {
        params.set(URL_PARAM_TAG, tagSelect.value);
      }

      if (activeSort === SORT_NEWEST) {
        params.set(URL_PARAM_SORT, SORT_NEWEST);
      }

      const url = new URL(window.location.href);

      url.search = params.toString();

      window.history.replaceState(
        window.history.state,
        "",
        `${url.pathname}${url.search}${url.hash}`,
      );
    };

    /**
     * Apply all active catalogue filters.
     */
    const updateCatalogue = () => {
      const filters = readActiveFilters();
      const visibleCount = applyCardVisibility(filters);

      updateSummary(visibleCount);
      updateClearButton(filters);
      updateEmptyState(visibleCount);
      syncUrlWithFilters(filters);
    };

    /**
     * Reset all controls and remove filter parameters from the URL.
     */
    const clearFilters = () => {
      searchInput.value = "";
      languageSelect.value = "";
      tagSelect.value = "";
      removeUrlFilterOptions(languageSelect);
      removeUrlFilterOptions(tagSelect);
      clearCatalogueUrlParameters();
      updateCatalogue();
      searchInput.focus();
    };

    searchInput.addEventListener("input", updateCatalogue);
    languageSelect.addEventListener("change", updateCatalogue);
    tagSelect.addEventListener("change", updateCatalogue);
    clearButton.addEventListener("click", clearFilters);

    sortButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const sort = sortFromButton(button);

        if (!sort || sort === activeSort) {
          return;
        }

        activeSort = sort === SORT_NEWEST ? SORT_NEWEST : SORT_ALPHA;
        setSortPressed(activeSort);
        applyCardOrder();
        updateCatalogue();
      });
    });

    catalogue.querySelectorAll(".catalogue-category").forEach((pill) => {
      if (pill.dataset.tagFilterBound === "true") {
        return;
      }

      pill.dataset.tagFilterBound = "true";
      pill.setAttribute(
        "aria-label",
        `Filter by ${pill.textContent?.trim() || "tag"}`,
      );

      pill.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();

        const label = pill.textContent?.trim() || "";

        if (!label) {
          return;
        }

        applySelectFilter(tagSelect, label);
        revealFilterPanel(filterPanel);
        updateCatalogue();
        tagSelect.focus({ preventScroll: true });
      });
    });

    catalogue
      .querySelectorAll("img.catalogue-logo[data-language]")
      .forEach((logo) => {
        if (logo.dataset.languageFilterBound === "true") {
          return;
        }

        const language = logo.dataset.language?.trim() || "";

        if (!language) {
          return;
        }

        logo.dataset.languageFilterBound = "true";

        let control = logo.closest("[data-language-filter-control]");

        if (!control) {
          control = document.createElement("button");
          control.type = "button";
          control.dataset.languageFilterControl = "";
          logo.replaceWith(control);
          control.append(logo);
        }

        const languageName = languageLabel(language);

        control.setAttribute("aria-label", `Filter by ${languageName}`);
        control.title = logo.getAttribute("title") || languageName;

        control.addEventListener("click", (event) => {
          event.preventDefault();
          event.stopPropagation();

          applySelectFilter(languageSelect, language);
          revealFilterPanel(filterPanel);
          updateCatalogue();
          languageSelect.focus({ preventScroll: true });
        });
      });

    activeSort = readSortFromUrl();
    setSortPressed(activeSort);
    applyCardOrder();
    applyInitialFilters();
    updateCatalogue();
  }

  onPageRender(initialiseCatalogue);
})();
