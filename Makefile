# Usage:
# make test  # run all tests
# make lint  # run all linters
# make format  # run black formatter


.PHONY = all test lint format

PYTHON_RUN := poetry run python -m


all: format lint test
	@echo "Done!"


test:
	${PYTHON_RUN} pytest --cov=deepip tests/


lint:
	${PYTHON_RUN} pylint deepip
	${PYTHON_RUN} pylint --disable=C0116,C0115,W0511,W0621,W0212 tests
	${PYTHON_RUN} black --check --verbose --diff .


format:
	${PYTHON_RUN} black .
