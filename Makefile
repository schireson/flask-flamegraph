.PHONY: install-deps lint sync-deps build test clean version

install-deps:
	pip install -r deps/dev-requirements.txt
	pip install -r deps/requirements.txt
	pip install --no-deps -e .

lint:
	bin/lint

sync-deps:
	pip install pip-tools

	pip-compile -o deps/dev-requirements.txt deps/dev-requirements.in
	pip-compile -o deps/requirements.txt deps/requirements.in

build:
	python setup.py bdist_wheel

test:
	pytest

clean:
	rm -f junit_results.xml .coverage
	rm -rf build dist coverage .mypy_cache .eggs

version:
	python setup.py -V
