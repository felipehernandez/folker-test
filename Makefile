setup:
	python3 -m venv ~/.folker-venv

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python3 -m unittest -v

lint:
	pylint folker