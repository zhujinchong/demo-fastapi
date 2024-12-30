# The builder image, used to build the virtual environment
FROM python:3.11-buster AS builder

RUN pip install poetry==1.8.5

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /workdir

COPY pyproject.toml poetry.lock ./

# -no-root：告诉Poetry不要安装我们的项目目录到虚拟环境中；否则会破坏Docker的层级缓存
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster AS runtime

ENV VIRTUAL_ENV=/workdir/.venv \
    PATH="/workdir/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app /workdir/app

ENTRYPOINT ["python", "/workdir/app/main.py"]
