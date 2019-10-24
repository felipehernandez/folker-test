FROM python:3.7

COPY folker folker
COPY ./folker.py folker.py
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ['python3', 'folker.py']