POETRY := poetry
MODULE_NAME := rfcdl
DIR_SRC := ./$(MODULE_NAME)

.PHONY: test
test: lint
	$(POETRY) run pytest -vv

.PHONY: lint
lint:
	$(POETRY) run flake8 .
	$(POETRY) run mypy
	$(POETRY) run vulture

.PHONY: format
format:
	$(POETRY) run black .
	$(POETRY) run isort .

.PHONY: setup
setup:
	$(POETRY) install --no-root

.PHONY: clean
clean:
	find -type d -name '.mypy_cache' -exec rm -rf {} +;
	find -type d -name '.pytest_cache' -exec rm -rf {} +;
	find -type d -name '__pycache__' -exec rm -rf {} +;
	rm -f ./tags

.PHONY: tags
tags:
	ctags -R \
		--extra=+f \
		--languages=Python \
		--sort=yes \
		--totals=yes \
		${DIR_SRC}
