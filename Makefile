.PHONY: lint
lint:
	flake8 ./glacier
	mypy ./glacier
	python3 -m unittest discover -v

.PHONY: clean
clean:
	rm -rf ./**/__pycache__
	rm -rf ./**/.mypy_cache
