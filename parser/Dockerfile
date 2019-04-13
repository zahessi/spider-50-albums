FROM python:3.7-alpine as base

RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                g++\
                libxslt-dev \
                libc-dev \
                linux-headers \
                mariadb-dev \
                musl-dev \
                libffi-dev \
                openssl-dev;

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /parser
WORKDIR /parser

ADD crontab.txt /crontab.txt
COPY entry.sh /entry.sh
RUN chmod 755 /entry.sh
RUN /usr/bin/crontab /crontab.txt

CMD ["/entry.sh"]
