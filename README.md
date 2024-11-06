# labs

<img src="https://img.shields.io/badge/runtime_revolution-labs-blue" />

## Topics

- [Architecture](docs/rag.md)
- [R&D](docs/rd.md)

## Getting Started

### Local Env

Create a copy of the reference env file in the root of the project and update the values accordingly.

`cp .env.sample .env.local`

### Test Env

Create a file named `.env.test` and the the following

```env
TEST_ENVIRONMENT=True

DATABASE_HOST=localhost
DATABASE_USER=postgres
DATABASE_PASS=postgres
DATABASE_NAME=test
DATABASE_PORT=65433
DATABASE_URL=postgresql://${DATABASE_USER}:${DATABASE_PASS}@${DATABASE_HOST}:${DATABASE_PORT}/${DATABASE_NAME}
```

## Run project

Here's the steps to setup the project locally:

1. `poetry shell`
2. `poetry install`
3. `make up`
4. `make ollama model=nomic-embed-text:latest`
5. `make ollama model=llama3.2:latest`
6. `make api` or `ENV=local make api`
7. `ENV=test make tests`
