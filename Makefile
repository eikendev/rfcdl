DIR_SRC=./rfcdl
DIR_TEST=./test

.PHONY: test
test: lint
	python3 -m pytest -vv

.PHONY: lint
lint:
	flake8 --ignore=E501 ${DIR_SRC}
	vulture-3 --exclude version.py ${DIR_SRC}
	mypy --ignore-missing-imports ${DIR_SRC}

.PHONY: clean
clean:
	find -type d -name '__pycache__' -exec rm -rf {} +;
	find -type d -name '.pytest_cache' -exec rm -rf {} +;
	find -type d -name '.mypy_cache' -exec rm -rf {} +;
	rm -rf ${DIR_TEST}/.cache
	rm -f tags

.PHONY: run
run:
	@python3 -m rfcdl

.PHONY: tags
tags:
	ctags -R \
		--sort=yes \
		--totals=yes \
		--languages=Python \
		--extra=+f \
		${DIR_SRC}
