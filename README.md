# labs

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Runtime Labs

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
4. `make api` or `ENV=local make api`
5. `ENV=test make tests`


## Project details

### Embeddings

During the course of the project, various approaches were taken regarding how embeddings are generated, namely:

* Splitting the files into predefined-sized chunks;
* Splitting the files according to the structure of the Python code they contain.

Although the results achieved are not as expected, since parts of the code are lost in the changes made by the LLM, the first method seems to yield results closer to the goal as fewer such losses occur.

For more details on the implementation and the test results, refer to the Jupyter Notebook [here](!https://github.com/runtimerevolution/labs/blob/main/notebooks/embeddings.ipynb).
