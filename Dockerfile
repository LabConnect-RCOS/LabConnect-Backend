FROM --platform=linux/amd64 python:3.12.4-alpine3.20

WORKDIR /app

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

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
