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
3. `make migrate`
4. `make load_fixtures`
5. `make createuser`

### Using OpenAI

1. `make up`
2. `make runserver`
3. `ENV=test make tests`

### Using Llama 3.2 with nomic:

1. `make up`
2. `make ollama model=nomic-embed-text:latest`
3. `make ollama model=llama3.2:latest`


### Using Starcoder2 with nomic:

1. `make up`
2. `make ollama model=nomic-embed-text:latest`
3. `make ollama model=starcoder2:15b-instruct`


### Using Qwen2.5 with nomic:

1. `make up`
2. `make ollama model=nomic-embed-text:latest`
3. `make ollama model=qwen2.5:7b-instruct`
