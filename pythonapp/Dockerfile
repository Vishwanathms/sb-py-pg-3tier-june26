# Simple Python container for pythonapp
FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir psycopg2-binary

COPY app.py /app/

EXPOSE 8080
CMD ["python", "app.py"]
