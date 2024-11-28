FROM python:3.11.6-slim-bookworm AS base

# Install poetry
RUN pip install pipx
RUN pip install gradio
RUN python3 -m pipx ensurepath
RUN pipx install poetry==1.8.3

ENV PATH="/root/.local/bin:$PATH"

# https://python-poetry.org/docs/configuration/#virtualenvsin-project
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

FROM base AS dependencies
WORKDIR /app
COPY pyproject.toml poetry.lock ./

FROM base AS app
ENV PYTHONUNBUFFERED=1
# ENV PORT=8000
ENV APP_ENV=prod
ENV PYTHONPATH="$PYTHONPATH:/private_gpt/"

COPY . /app
WORKDIR /app

ARG POETRY_EXTRAS="ui vector-stores-postgres llms-azopenai embeddings-azopenai"
RUN poetry install --no-root --extras "${POETRY_EXTRAS}"
ENV GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_NAME=0.0.0.0
EXPOSE 7860:7860

ENTRYPOINT ["poetry", "run", "python", "-m", "private_gpt"]