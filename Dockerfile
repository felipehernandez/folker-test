FROM python:3.8-slim

COPY folker folker
COPY ./folker.py folker.py
COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 -m unittest -v

# For testing
#COPY example/test/protos protos
#COPY example example
#RUN python3 folker.py -t

WORKDIR /

ENTRYPOINT ["python", "folker.py"]