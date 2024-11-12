# `python-base` sets up all our shared environment variables
FROM python:3.12.5-slim AS python-base

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# `builder-base` stage is used to build deps
FROM python-base AS builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH

# Install production dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --no-dev


# `production` image
FROM python-base AS production

# Install git since gitpython needs a git executable
RUN apt-get update && apt-get install --no-install-recommends -y git

# Copy our built venv
COPY --from=builder-base $VENV_PATH $VENV_PATH

# Copy the app into /app
WORKDIR /app

COPY ./labs/ /app/

CMD python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000
