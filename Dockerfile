# Aplicando Multi-stage build
## ------------------------------- Pre Production Stage ------------------------------ ## 
FROM python:3.13-bookworm AS pre-production

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY ./pyproject.toml .

RUN uv sync

## ------------------------------- Production Stage ------------------------------ ## 
FROM python:3.13-slim-bookworm AS production

RUN useradd --create-home app_user
USER app_user

WORKDIR /app

COPY /src src
COPY --from=pre-production /app/.venv .venv

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE $PORT

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]