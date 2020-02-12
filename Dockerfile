FROM python:3.8-slim

COPY folker folker
COPY ./folker.py folker.py
COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 -m unittest -v

ENTRYPOINT ["python", "folker.py"]