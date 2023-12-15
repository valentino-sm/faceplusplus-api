FROM python:3.11-slim as base
WORKDIR /app/
ENV PATH="/app/venv/bin:$PATH"
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y git && \
  rm -rf /var/lib/apt/lists/*
RUN python -m venv venv && pip install --no-cache-dir poetry==1.7.1
COPY poetry.lock pyproject.toml ./  
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

FROM python:3.11-slim as app
LABEL author=valentino-sm
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl ffmpeg libsm6 libxext6 && \
  rm -rf /var/lib/apt/lists/*
WORKDIR /app/
ENV PATH="/app/venv/bin:$PATH"
COPY --from=base /app/venv venv
COPY . .
EXPOSE 8000
