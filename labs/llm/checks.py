import json
import logging

from parsers.response import parse_llm_output
from pydantic import ValidationError as PydanticValidationError

logger = logging.getLogger(__name__)


class ValidationError(ValueError):
    pass


def check_length(llm_response):
    finish_reason = getattr(llm_response["choices"][0]["message"], "finish_reason", None)
    if finish_reason == "length":
        raise ValidationError("Conversation was too long for the context window, resulting in incomplete JSON.")


def check_content_filter(llm_response):
    finish_reason = getattr(llm_response["choices"][0]["message"], "finish_reason", None)
    if finish_reason == "content-filter":
        raise ValidationError(
            "Model's output included restricted content. Generation of JSON was halted and may be partial."
        )


def check_refusal(llm_response):
    refusal_reason = getattr(llm_response["choices"][0]["message"], "refusal", None)
    if refusal_reason:
        raise ValidationError(f"OpenAI safety system refused the request. Reason: {refusal_reason}")


def check_invalid_json(llm_response):
    response_content = llm_response["choices"][0]["message"]["content"]
    try:
        json.loads(response_content)
    except ValueError:
        raise ValidationError("Malformed JSON LLM response.")

    try:
        parse_llm_output(response_content)

    except PydanticValidationError:
        raise ValidationError("JSON response from LLM does not match the expected format.")


check_list = [
    check_length,
    check_content_filter,
    check_refusal,
    check_invalid_json,
]


def run_response_checks(llm_response):
    for check in check_list:
        logger.debug(f"Running LLM response check {check.__name__}")

        try:
            check(llm_response[1])

        except ValidationError as validation_error:
            return True, str(validation_error)

        except Exception as error:
            return True, str(error)

    return False, ""
