# labs

<img src="https://img.shields.io/badge/runtime_revolution-labs-blue" />

## Topics

- [Architecture](docs/rag.md)
- [R&D](docs/rd.md)

## Getting Started

### Local Env

Create a copy of the reference env file in the root of the project and update the values accordingly.

`cp .env.sample .env`

### Pre-commit

Make sure you have pre-commit installed [docs](https://pre-commit.com/).

Then run the following command to set up the project's git hook scripts

```bash
pre-commit install
```

To run against all files you can use the following command

```bash
pre-commit run --all-files
```

## Run project

Here's the steps to set up the project locally:

1. `poetry shell`
2. `poetry install`
3. `make up`
4. `make setup`
5. Go to [http://localhost:8000/admin](http://localhost:8000/admin) in internet browser and login (admin/admin)
6. Select "Variables" option in the menu on the left and fill in the "OPENAI_API_KEY" key value with your [OpenAI API Key](https://openai.com/index/openai-api/) and click "Save"
7. Click the "Add" button of the "Project" option in the menu on the left and fill in the "Name" and select the "Project directory" and click "Save" in red boxes in image bellow:
   ![new_project_fields](docs/assets/new_project_fields.png)

## Run with dev container

1. Reopen in container / Open folder in container
2. `poetry shell`
3. `make up`
4. `make setup`

## Run with local models

### Using OpenAI

1. `make up`
2. `make migrate`
3. `make loadfixtures`
4. `make createuser`
5. Go to [http://localhost:8000/admin](http://localhost:8000/admin) in internet browser and login (admin/admin)
6. Select "Variables" option in the menu on the left and fill in the "OPENAI_API_KEY" key value with your [OpenAI API Key](https://openai.com/index/openai-api/) and click "Save"

### Using Llama 3.2 with nomic:

1. `make up`
2. `make createuser`
3. `make ollama model=nomic-embed-text:latest`
4. `make ollama model=llama3.2:latest`
5. Go to [http://localhost:8000/admin](http://localhost:8000/admin) in internet browser and login (admin/admin)
6. Select "Models" option in the menu on the left
7. Fill in the models name and check the "active" checkbox in red boxes in the image bellow and click "Save" (pay attention to the LLM and Embeddings model name placement):
   ![local_models_admin_fields](docs/assets/local_models_admin_fields.png)

### Using Starcoder2 with nomic:

1. `make up`
2. `make createuser`
3. `make ollama model=nomic-embed-text:latest`
4. `make ollama model=starcoder2:15b-instruct`
5. Go to [http://localhost:8000/admin](http://localhost:8000/admin) in internet browser and login (admin/admin)
6. Select "Models" option in the menu on the left
7. Fill in the models name and check the "active" checkbox in red boxes in the image bellow and click "Save" (pay attention to the LLM and Embeddings model name placement):
   ![local_models_admin_fields](docs/assets/local_models_admin_fields.png)

### Using Qwen2.5 with nomic:

1. `make up`
2. `make createuser`
3. `make ollama model=nomic-embed-text:latest`
4. `make ollama model=qwen2.5:7b-instruct`
5. Go to [http://localhost:8000/admin](http://localhost:8000/admin) in internet browser and login (admin/admin)
6. Select "Models" option in the menu on the left
7. Fill in the models name and check the "active" checkbox in red boxes in the image bellow and click "Save" (pay attention to the LLM and Embeddings model name placement):
   ![local_models_admin_fields](docs/assets/local_models_admin_fields.png)

### Using DeepSeek R1 with nomic:

1. `make up`
2. `make createuser`
3. `make ollama model=nomic-embed-text:latest`
4. `make ollama model=deepseek-r1` | `deepseek-coder` | `deepseek-coder-v2`, coder-v2 is the best if you have a good machine.
5. Go to [http://localhost:8000/admin](http://localhost:8000/admin) in internet browser and login (admin/admin)
6. Select "Models" option in the menu on the left
7. Fill in the models name and check the "active" checkbox in red boxes in the image below and click "Save" (pay attention to the LLM and Embeddings model name placement):
   ![local_models_admin_fields](docs/assets/local_models_admin_fields.png)

## Prompt Examples

There are some prompt examples in [here](docs/prompt_examples.md). These are sorted by complexity and are a way for us to measure the quality of the LLM's response.
