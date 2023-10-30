FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    APP_VERSION=3.0.0

RUN mkdir /code
WORKDIR /code
COPY . .

RUN apk add --no-cache --virtual .build-deps \
    g++ gcc \
    && pip install -r requirements.txt \
    && apk del .build-deps

EXPOSE 8000

RUN pip install gunicorn

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "BanPay.wsgi:application" ]