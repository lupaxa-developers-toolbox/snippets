.PHONY: snippets-lint-runnable check

snippets-lint-runnable:
	$(PYTHON) -m snippets_mkdocs.lint

check: snippets-lint-runnable
