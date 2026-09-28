FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml requirements.lock README.md ./
COPY app ./app

RUN pip install --no-cache-dir -r requirements.lock \
    && pip install --no-cache-dir --no-deps .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
