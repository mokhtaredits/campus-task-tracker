# syntax=docker/dockerfile:1
FROM python:3.13-slim AS build
WORKDIR /build
COPY requirements.txt .
RUN python -m pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

FROM python:3.13-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TASK_DB=/app/data/tasks.db
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=bind,from=build,source=/wheels,target=/wheels \
    python -m pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && mkdir /app/data \
    && chown 10001:10001 /app/data
COPY src/ ./src/
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s --start-period=10s --retries=5 \
    CMD ["python", "-c", "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health', timeout=2).close()"]
CMD ["waitress-serve", "--listen=0.0.0.0:8000", "src.app:app"]
