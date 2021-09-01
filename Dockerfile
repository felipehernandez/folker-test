FROM python:3.9-slim

WORKDIR /

RUN pip install --upgrade pip

COPY folker folker
COPY ./setup.py setup.py
RUN pip install -e .

WORKDIR /

ENTRYPOINT ["folker-test"]