FROM python:3.12-slim

WORKDIR /app

COPY backend /app/backend
COPY web /app/web

RUN pip install --no-cache-dir -r /app/web/requirements.txt

ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "10000"]
