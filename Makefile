# Usage:
# make test  # run all tests


.PHONY = test


test:
	python3 -m pytest --cov=deepip tests/


lint:
	python3 -m pylint deepip
	python3 -m pylint --disable=C0116,C0115,W0511,W0621,W0212 tests
	python3 -m black --check --verbose --diff .


format:
	python3 -m black .
