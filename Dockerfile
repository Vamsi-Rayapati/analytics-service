FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_SYSTEM_PYTHON=1
ENV UV_NO_CACHE=1

# analytics-common is copied first so it can be installed as a local dependency
COPY analytics-common /analytics-common
COPY analytics-service/pyproject.toml analytics-service/uv.lock ./
RUN uv pip install -e /analytics-common && \
    uv sync --frozen --no-dev

COPY analytics-service/ .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
