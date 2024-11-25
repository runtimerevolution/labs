# labs

<img src="https://img.shields.io/badge/runtime_revolution-labs-blue" />

## Topics

- [Architecture](docs/rag.md)
- [R&D](docs/rd.md)

## Getting Started

### Local Env

Create a copy of the reference env file in the root of the project and update the values accordingly.

`cp .env.sample .env.local`

## Run project

Here's the steps to set up the project locally:

1. `poetry shell`
2. `poetry install`

### Using OpenAI

1. `make up`
2. `make api` or `ENV=local make api`
3. `ENV=test make tests`

### Using Llama 3.2 with nomic:

1. `export LOCAL_LLM=True`
2. `make up`
3. `make ollama model=nomic-embed-text:latest`
4. `make ollama model=llama3.2:latest`


### Using Starcoder2 with nomic:

1. `export LOCAL_LLM=True`
2. `make up`
3. `make ollama model=nomic-embed-text:latest`
4. `make ollama model=starcoder2:7b`
