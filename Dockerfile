
FROM python:3.10-alpine

ADD . /mystalker
WORKDIR /mystalker

RUN pip install -e .

ENTRYPOINT [ "python3.10", "-u", "/mystalker/mystalker.py" ]
