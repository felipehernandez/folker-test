FROM python:3.9-slim

WORKDIR /

RUN pip install --upgrade pip

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY folker folker
COPY ./setup.py setup.py
RUN pip install -e .

WORKDIR /

ENTRYPOINT ["folker"]