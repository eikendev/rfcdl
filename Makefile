PYTHON := python3
DIR_SRC := ./rfcdl

.PHONY: test
test: lint
	${PYTHON} -m pytest -vv

.PHONY: lint
lint:
	${PYTHON} -m flake8 --ignore=E501 ${DIR_SRC}
	${PYTHON} -m vulture --exclude version.py ${DIR_SRC}
	${PYTHON} -m mypy --ignore-missing-imports ${DIR_SRC}

.PHONY: setup
setup:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

.PHONY: clean
clean:
	find -type d -name '__pycache__' -exec rm -rf {} +;
	find -type d -name '.pytest_cache' -exec rm -rf {} +;
	find -type d -name '.mypy_cache' -exec rm -rf {} +;
	rm -f ./tags

.PHONY: run
run:
	${PYTHON} -m rfcdl

.PHONY: tags
tags:
	ctags -R \
		--sort=yes \
		--totals=yes \
		--languages=Python \
		--extra=+f \
		${DIR_SRC}
