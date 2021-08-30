FROM python:3.9-slim

WORKDIR /

COPY folker folker
COPY ./setup.py setup.py
COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .

WORKDIR /

ENTRYPOINT ["folker"]