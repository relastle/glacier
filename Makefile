.PHONY: lint
lint:
	flake8 ./glacier
	mypy ./glacier
	python -m unittest discover -v

.PHONY: clean
clean:
	rm -rf ./**/__pycache__
	rm -rf ./**/.mypy_cache
