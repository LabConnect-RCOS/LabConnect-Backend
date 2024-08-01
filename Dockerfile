FROM --platform=linux/amd64 python:3.12.4-alpine3.20

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY labconnect /app/labconnect
COPY run.py .
COPY db_init.py .
COPY config.py .

EXPOSE 8000

CMD ["gunicorn", "run:app", "--bind", "0.0.0.0", "-w", "6", "--preload", "--max-requests-jitter", "300"]
