# Research & Development

This document aims to document some of the approaches tested and the discoveries made on various problems, 
as well as the results achieved from the tests conducted.


## Embeddings

During the course of the project, various approaches were taken regarding how embeddings are generated, namely:

* Splitting the files into predefined-sized chunks (**File chunks**);
* Splitting the files according to the structure of the Python code they contain (**Python code structured**).

For more details on the implementation and the test results, refer to the Jupyter Notebook [here](../notebooks/embeddings.ipynb).

## Test results

The following table consisely presents the results obtained where:
* **Embeddings model**: indicates the model used to generate the embeddings;
* **LLM**: indicates the LLM used, which can be either a Local LLM or via an external API (like OpenAI);
* **Embeddings creation method**: indicates the method used to create embeddings, as previously described;
* **Response quality**: indicates the quality of the LLM's response, which can be:
  * **Very poor**: The code contains critical issues such as syntax errors, missing imports or broken logic 
  that prevent it from running;
  * **Poor**: The code runs but fails to achieve the intended result. It contains logical error or incorrect 
  implementation of functions, and often throws runtime errors;
  * **Average**: The code is mostly functional, but there are some errors or edge cases where it fails. 
  It produces the desired result in many scenarios but may have inefficiencies, unhandled exceptions, 
  or inconsistent behavior in certain conditions;
  * **Good**: The code works as expected to the majority of the cases and handles most inputs correctly. 
  It follows good practices and has few, if any, logical errors but might lack optimization or robustness in edge cases;
  * **Excellent**: The code is flawless and functions exactly as expected across all scenarios.
  It is well-structured, optimized and follows Python best practices;
* **Prompt**: indicates the prompt used in the LLM.


| Embedding model                                                                               | LLM (Local/API)                                                         | Embeddings creation method | Response quality | Prompt   | Notes/Observations                                                  |
|-----------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|----------------------------|------------------|----------|---------------------------------------------------------------------|
| [text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings/embedding-models) | OpenAI API                                                              | File chunks                | Average          | Prompt 1 |                                                                     |
| [text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings/embedding-models) | OpenAI API                                                              | Python code structure      | Average          | Prompt 1 |                                                                     |
| [nomic-embed-text](https://ollama.com/library/nomic-embed-text)                               | Local: [starcoder2:15b-instruct](https://ollama.com/library/starcoder2) | File chunks                | Poor             | Prompt 1 |                                                                     |
| [nomic-embed-text](https://ollama.com/library/nomic-embed-text)                               | Local: [qwen2.5:7b-instruct](https://ollama.com/library/qwen2.5)        | File chunks                | Poor             | Prompt 1 | The requested JSON in `Prompt 1` was poorly formatted or incorrect. |
| [text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings/embedding-models) | OpenAI API                                                              | Python code structure      | Good             | Prompt 2 | Read the Note 1 in Notes/observations                               |


Below is the prompt used in the LLM for the test conducted:

#### Prompt 1:
> You're a diligent software engineer AI. You can't see, draw, or interact with a 
> browser, but you can read and write files, and you can think. 
> You've been given the following task: Add created_at and updated_at field to User model. 
> Any imports will be at the beggining of the file. 
> Add tests for the new functionalities, considering any existing test files. 
> The file paths provided are **absolute paths relative to the project root**, 
> and **must not be changed**. Ensure the paths you output match the paths provided exactly. 
> Do not prepend or modify the paths. 
> Please provide a json response in the following format: {{"steps": [...]}} 
> Where steps is a list of objects where each object contains three fields:
> type, which is either 'create' to add a new file or 'modify' to edit an existing one; 
> If the file is to be modified send the finished version of the entire file. 
> path, which is the absolute path of the file to create/modify; 
> content, which is the content to write to the file.


#### Prompt 2:
> You are an advanced Python coding assistant designed to resolve tasks for Python-based code. 
> You will receive:
>     1. A description of the task.
>     2. File names and their contents as context (already provided in the system message).
>     3. Constraints such as not modifying migrations unless explicitly required.
> 
> You should:
>     - Analyze the provided task description and associated context.
>     - Generate the necessary Python code changes to resolve the task.
>     - Ensure adherence to Python best practices.
>     - Avoid changes to migrations or unrelated files unless specified.
>     - Provide clean, organized, and ready-to-review code changes.
>     - Group related logic together to ensure clarity and cohesion.
>     - Add meaningful comments to explain non-obvious logic or complex operations.
>     - Ensure the code integrates seamlessly into the existing structure of the project.
> 
> Task description:
>     {issue_summary}
>   
> Based on the task description and the provided system context:
>     - Write the Python code changes required to resolve the task.
>     - Ensure that changes are made only within the allowed scope.
>    
> You must provide a JSON response in the following format: {JSON_RESPONSE}
>    
> Perform the 'delete' operations in reverse line number order to avoid line shifting.


### Notes/Observations:

#### Note 1

Although the results are quite accurate when using the prompt **"Add created_at and updated_at fields to the User 
model"**, small errors occasionally occur, such as:

```python
...
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)    datetime_field = models.DateTimeField(blank=True, null=True)
...
```
Where a \n is missing after the updated_at field, causing the code to be incorrect.

Another error that occasionally happens when using the prompt "Add tests to created_at and updated_at fields in the 
User model" is that the code is placed in the correct file and class but mixed with other test code.
The code snippet below (incomplete) illustrates this behavior:

```python
...
class UserTest(TestCase):
    def test_one:
        <lines of code of test_one>
    def llm_added_test:
        ...
        <lines of code of test_one>
...
```

Other prompts tested include:

* **"Remove the created_at and updated_at at User model"**
* **"Remove created_at and updated_at fields to User model"**
* **"Add created_at and updated_at fields to User admin model"**
* **"Remove created_at and updated_at fields at User admin model"**

In general, and after several tests conducted with the described prompts, the results have been as expected and satisfactory.
