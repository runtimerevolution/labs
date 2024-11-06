# Research & Development

This document aims to document some of the approaches tested and the discoveries made on various problems, 
as well as the results achieved from the tests conducted.


## Embeddings

During the course of the project, various approaches were taken regarding how embeddings are generated, namely:

* Splitting the files into predefined-sized chunks (**File chunks**);
* Splitting the files according to the structure of the Python code they contain (**Python code structured**).

For more details on the implementation and the test results, refer to the Jupyter Notebook [here](../notebooks/embeddings.ipynb).

### Test results

The following table consisely presents the results obtained where:
* **Embeddins model**: indicates the model used to generate the embeddings;
* **LLM**: indicates the LLM used, which can be either a Local LLM or via an external API (like OpenAI);
* **Embeddins creation method**: indicates the method used to create embeddins, as previously described;
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


| Embedding model                                                                               | LLM (Local/API) | Embeddins creation method | Response quality | Prompt   |
|-----------------------------------------------------------------------------------------------|-----------------|---------------------------|------------------|----------|
| [text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings/embedding-models) | OpenAI API      | File chunks               | Poor             | Prompt 1 |
| [text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings/embedding-models) | OpenAI API      | Python code structure     | Poor             | Prompt 1 |


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
