FROM python:3.12.0-alpine3.18

WORKDIR /home/python/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --no-cache gcc make \
    && rm -rf /var/cache/apk/*

RUN pip install --upgrade pip

RUN pip install poetry

COPY . .

RUN poetry install

CMD tail -f /dev/null
