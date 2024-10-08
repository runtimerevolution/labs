FROM python:3.12.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app/

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false && poetry install

COPY . /app/

RUN adduser pythonappuser
USER pythonappuser
