ALLURE_RESULTS := reports/allure-results

.PHONY: install lint format test-local lock

install:
	poetry install
	poetry run pre-commit install

lint:
	poetry run ruff check .
	poetry run ruff format --check .

format:
	poetry run ruff check --fix .
	poetry run ruff format .

test-local:
	-poetry run pytest --alluredir=$(ALLURE_RESULTS) -m "$(mark)" $(ARGS)
	allure serve $(ALLURE_RESULTS)

lock:
	poetry lock
	poetry install
