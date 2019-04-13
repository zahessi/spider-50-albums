FROM python:3.7-alpine

RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                musl-dev \
                libffi-dev \
                openssl-dev;


COPY requirements.txt /
RUN pip install -r /requirements.txt

EXPOSE 8443
COPY . /code
WORKDIR /code
CMD ["python", "main.py"]
