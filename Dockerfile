FROM python:3.10-slim

RUN pip install --no-cache-dir flask spotipy requests

WORKDIR /app

COPY app.py .
COPY templates ./templates

EXPOSE 5001

CMD ["python", "app.py"]

