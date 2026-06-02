FROM python:3.13.1-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        tdsodbc \
        git \
        libkrb5-dev \
    && python -m pip install --no-cache-dir --upgrade pip \
    && pip install uv

WORKDIR /code/

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

RUN apt-get autoremove -yqq --purge \
    && apt-get clean -yqq \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY . /code/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

EXPOSE 8050

ENV PATH="/code/.venv/bin:$PATH"

CMD ["python", "index.py"]
