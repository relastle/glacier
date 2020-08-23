.PHONY: lint
lint:
	flake8 ./water
	mypy ./water
	python -m unittest discover -v

.PHONY: clean
clean:
	rm -rf ./**/__pycache__
	rm -rf ./**/.mypy_cache
