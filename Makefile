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
	coverage html -d reports/coverage --title=report --omit="*/lib/python*"

lint:
	pylint folker

integration-all:
	make integration-code
	make integration-conditional
	make integration-datastore
	make integration-file
	make integration-foreach
	make integration-gmail
	make integration-graphql
	make integration-grpc
	make integration-kafka
	make integration-parallel
	make integration-print
	make integration-postgres
	make integration-profile
	make integration-protobuf
	make integration-pubsub
	make integration-rabbitmq
	make integration-rest
	make integration-save
	make integration-template
	make integration-void
	make integration-wait
	make integration-zookeeper
integration-code:
	cp -R example/code/ testcode
	python folker/cli.py -t code -n 1 # --trace
	rm -R testcode
integration-conditional:
	python folker/cli.py -t conditional -n 1 # --trace
integration-datastore:
	cp -R example/credentials/ credentials
	python folker/cli.py -t datastore -n 4 # --trace
	rm -R credentials
integration-file:
	python folker/cli.py -t file -n 1 # --trace
integration-foreach:
	python folker/cli.py -t foreach -n 1 # --trace
integration-gmail:
	python folker/cli.py -t gmail -n 1 # --trace
integration-graphql:
	python folker/cli.py -t graphql -n 1 # --trace
integration-grpc:
	cp -R example/protos/ protos
	python folker/cli.py -t grpc -n 1 # --trace
	rm -R protos
integration-kafka:
	python folker/cli.py -t kafka -n 1 # --trace
integration-parallel:
	python folker/cli.py -t parallel -n 3 # --trace
integration-print:
	python folker/cli.py -t print -n 2 # --trace
integration-postgres:
	python folker/cli.py -t postgres -n 1 # --trace
integration-profile:
	python folker/cli.py -p test-profile -t profile -n 1 # --trace
integration-protobuf:
	cp -R example/protos/ protos
	python folker/cli.py -t protobuf -n 2 # --trace
	rm -R protos
integration-pubsub:
	python folker/cli.py -t pubsub -n 1 # --trace
integration-rabbitmq:
	python folker/cli.py -t rabbitmq -n 4 # --trace
integration-rest:
	cp -R example/protos/ protos
	python folker/cli.py -t rest -n 3 # --trace
	rm -R protos
integration-save:
	python folker/cli.py -t save -n 2 # --trace
integration-template:
	python folker/cli.py -t template -n 3 # --trace
integration-void:
	python folker/cli.py -t void -n 3 # --trace
integration-wait:
	python folker/cli.py -t wait -n 1 # --trace
integration-zookeeper:
	python folker/cli.py -t zookeeper -n 4 # --trace
