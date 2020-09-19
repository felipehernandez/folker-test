setup:
	python3 -m venv ~/.folker-venv

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	coverage run -m pytest -vv
	coverage report -m

test-report:
	coverage run -m pytest -vv
	coverage html -d reports/coverage --title=report --skip-covered --skip-empty

lint:
	pylint folker