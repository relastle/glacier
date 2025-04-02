.PHONY: lint
lint:
	ruff check ./glacier ./tests
	mypy ./glacier ./tests

.PHONY: test
test:
	coverage run --omit='./tests/**/*' --source=. -m pytest -vvs --durations=10
	coverage report -m

.PHONY: publish
publish: lint
	python -m build
	twine upload dist/* -u __token__ -p ${PYPI_TOKEN}

.PHONY: clean
clean:
	rm -rf ./**/__pycache__
	rm -rf ./**/.mypy_cache
	rm -rf ./dist
	rm -rf ./build
	rm -rf ./.venv
