FROM python:3.14-slim-trixie

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    build-essential \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

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
