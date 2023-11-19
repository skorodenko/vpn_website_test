FROM python:3.11-slim-buster AS builder

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./

RUN poetry install --without=dev --no-root && rm -rf $POETRY_CACHE_DIR


FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/.venv \
    PATH=/.venv/bin:$PATH

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY . .