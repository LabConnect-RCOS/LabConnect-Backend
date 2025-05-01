FROM python:3.13-alpine

WORKDIR /app

RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    libxml2-dev \
    libxslt-dev \
    xmlsec-dev \
    pkgconfig \
    libtool \
    autoconf \
    automake \
    make \
    libffi-dev \
    openssl-dev \
    python3-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY labconnect/ /app/labconnect/
COPY migrations/ /app/migrations/
COPY app.py .
COPY db_init.py .
COPY config.py .
COPY run.sh .
RUN chmod +x run.sh

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://0.0.0.0:9000 || exit 1

EXPOSE 9000

CMD ["/app/run.sh"]
