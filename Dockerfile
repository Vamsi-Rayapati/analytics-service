FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_SYSTEM_PYTHON=1
ENV UV_NO_CACHE=1

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

EXPOSE 4000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000", "--reload"]
