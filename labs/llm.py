import logging

from core.models import Model, VectorizerModel
from decorators import time_and_log_function
from embeddings.embedder import Embedder
from embeddings.vectorizers.base import Vectorizer
from litellm_service.llm_requester import Requester
from parsers.response_parser import is_valid_json, parse_llm_output

logger = logging.getLogger(__name__)


def get_prompt(issue_summary):
    return f"""
        You're a diligent software engineer AI. You can't see, draw, or interact with a 
        browser, but you can read and write files, and you can think.
        You've been given the following task: {issue_summary}.
        Any imports will be at the beggining of the file.
        Add tests for the new functionalities, considering any existing test files.
        The file paths provided are **absolute paths relative to the project root**, 
        and **must not be changed**. Ensure the paths you output match the paths provided exactly. 
        Do not prepend or modify the paths.
        Please provide a json response in the following format: {{"steps": [...]}}
        Where steps is a list of objects where each object contains three fields:
        type, which is either 'create' to add a new file or 'modify' to edit an existing one;
        If the file is to be modified send the finished version of the entire file.
        path, which is the absolute path of the file to create/modify;
        content, which is the content to write to the file.
    """


def prepare_context(context, prompt):
    prepared_context = []
    for file in context:
        prepared_context.append(
            {
                "role": "system",
                "content": f"File: {file[1]} Content: {file[2]}",
            }
        )
    prepared_context.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    return prepared_context


def check_length_issue(llm_response):
    finish_reason = getattr(llm_response["choices"][0]["message"], "finish_reason", None)
    if finish_reason == "length":
        return (
            True,
            "Conversation was too long for the context window, resulting in incomplete JSON.",
        )
    return False, ""


def check_content_filter(llm_response):
    finish_reason = getattr(llm_response["choices"][0]["message"], "finish_reason", None)
    if finish_reason == "content_filter":
        return (
            True,
            "Model's output included restricted content. Generation of JSON was halted and may be partial.",
        )
    return False, ""


def check_refusal(llm_response):
    refusal_reason = getattr(llm_response["choices"][0]["message"], "refusal", None)
    if refusal_reason:
        return (
            True,
            f"OpenAI safety system refused the request. Reason: {refusal_reason}",
        )
    return False, ""


def check_invalid_json_response(llm_response):
    response_string = llm_response["choices"][0]["message"]["content"]
    if not is_valid_json(response_string):
        return True, "Invalid JSON response."
    else:
        if not parse_llm_output(response_string):
            return True, "Invalid JSON response."
        return False, ""


validation_checks = [
    check_length_issue,
    check_content_filter,
    check_refusal,
    check_invalid_json_response,
]


def validate_llm_response(llm_response):
    for check in validation_checks:
        logger.debug(llm_response)
        is_invalid, message = check(llm_response[1])
        if is_invalid:
            return True, message
    return False, ""


def get_llm_response(prepared_context):
    llm_requester, *llm_requester_args = Model.get_active_llm_model()

    retries, max_retries = 0, 5
    redo, redo_reason = True, None
    requester = Requester(llm_requester, *llm_requester_args)

    while redo and retries < max_retries:
        try:
            llm_response = requester.completion_without_proxy(prepared_context)
            logger.debug(f"LLM Response: {llm_response}")
            redo, redo_reason = validate_llm_response(llm_response)
        except Exception:
            redo, redo_reason = True, "Error calling LLM."
            logger.exception(redo_reason)

        if redo:
            retries = retries + 1
            logger.info(f"Redoing request due to {redo_reason}")

    if retries == max_retries:
        logger.info("Max retries reached.")
        return False, None
    return True, llm_response


@time_and_log_function
def call_llm_with_context(repo_destination, issue_summary):
    if not issue_summary:
        logger.error("issue_summary cannot be empty.")
        raise ValueError("issue_summary cannot be empty.")

    embedder_class, *embeder_args = Model.get_active_embedding_model()
    embedder = Embedder(embedder_class, *embeder_args)

    vectorizer_class = VectorizerModel.get_active_vectorizer()
    Vectorizer(vectorizer_class, embedder).vectorize_to_database(None, repo_destination)

    # find_similar_embeddings narrows down codebase to files that matter for the issue at hand.
    context = embedder.retrieve_embeddings(issue_summary, repo_destination)

    prompt = get_prompt(issue_summary)
    prepared_context = prepare_context(context, prompt)

    logger.debug(f"Issue Summary: {issue_summary} - LLM Model: {embeder_args[0]}")

    return get_llm_response(prepared_context)
