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
EXPOSE 8443
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
