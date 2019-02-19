FROM python:3.7-alpine

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
ADD . /parser
WORKDIR /parser
RUN pip install -r requirements.txt
CMD ["python", "-u", "run.py"]
