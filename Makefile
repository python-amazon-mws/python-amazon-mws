.PHONY: install-dev lint test cover wheel wheel-lint clean upload-to-pypi-test upload-to-pypi

install-dev:
	pip install -r requirements.txt
	pip install -e .

lint:
	flake8

test:
	pytest

cover:
	pytest --cov=mws

wheel:
	python setup.py sdist bdist_wheel

wheel-lint: wheel
	twine check dist/*

clean:
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf mws.egg-info/
	rm -f .coverage

upload-to-pypi-test: clean wheel-lint
	twine upload \
		--repository-url https://test.pypi.org/legacy/ \
		--sign \
		dist/*

upload-to-pypi: clean wheel-lint
	twine upload \
		--sign \
		dist/*