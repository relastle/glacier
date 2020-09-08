.PHONY: lint
lint:
	flake8 ./glacier ./tests
	mypy ./glacier ./tests
	python3 -m unittest discover -v

.PHONY: test
test:
	coverage run --omit='./tests/**/*' --source=. -m pytest -vvs --durations=10 --diff-type=split
	coverage report -m

.PHONY: publish
publish: lint
	@poetry build
	@poetry publish -u ${PYPI_USER} -p ${PYPI_PASSWORD}

.PHONY: clean
clean:
	rm -rf ./**/__pycache__
	rm -rf ./**/.mypy_cache
