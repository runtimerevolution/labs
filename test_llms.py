import json
import time

from labs.config import LITELLM_API_KEY
from litellm_service.request import RequestLiteLLM


dic = {
    "hello_world.json": 'Add a file to print sentence "Hello World"',
    "calculator.json": "Add a simple calculator",
}

models = [
    "openai/gpt-3.5-turbo",
    "gemini/gemini-pro",
    "huggingface/mistralai/Mistral-7B-Instruct-v0.1",
    # RESTRICTED MODEL "huggingface/meta-llama/Llama-2-7b",
    "huggingface/tiiuae/falcon-7b-instruct",
    # MODEL IS TOO LARGE TO BE LOADED "huggingface/mosaicml/mpt-7b-chat",
    # LIMITED BY 8192 TOKENS "huggingface/codellama/CodeLlama-34b-Instruct-hf",
    # MODEL IS TOO LARGE TO BE LOADED "huggingface/WizardLM/WizardCoder-Python-34B-V1.0",
    # MODEL IS TOO LARGE TO BE LOADED "huggingface/Phind/Phind-CodeLlama-34B-v2",
    # NEEDS BILLING TO BE ACTIVATED "anthropic/claude-2",
    # NEEDS BILLING TO BE ACTIVATED "anthropic/claude-instant-1.2",
    # NEEDS BILLING TO BE ACTIVATED "anthropic/claude-instant-1",
    # TOKEN RESTRICTED "groq/llama3-8b-8192",
    # TOKEN RESTRICTED "groq/llama3-70b-8192",
    # TOKEN RESTRICTED "groq/llama2-70b-4096",
    # TOKEN RESTRICTED "groq/mixtral-8x7b-32768",
    # TOKEN RESTRICTED "groq/gemma-7b-it",
    "command-r",
    "command-light",
    "command-r-plus",
    # litellm.BadRequestError: LLM Provider NOT provided "command-medium",
    # model 'command-medium-beta' not found "command-medium-beta",
    # litellm.BadRequestError: LLM Provider NOT provided. "command-xlarge-nightly",
    "command-nightly",
    # 400 EXCEPTION "anyscale/meta-llama/Llama-2-7b-chat-hf",
    # 400 EXCEPTION "anyscale/meta-llama/Llama-2-13b-chat-hf",
    # 400 EXCEPTION "anyscale/meta-llama/Llama-2-70b-chat-hf",
    # 400 EXCEPTION "anyscale/mistralai/Mistral-7B-Instruct-v0.1",
    # 400 EXCEPTION "anyscale/codellama/CodeLlama-34b-Instruct-hf",
]


def load_file(file_name):
    the_file = open(file_name, "r")
    bla = the_file.read()
    result = json.loads(bla)
    the_file.close()
    return result


def test():
    litellm_requests = RequestLiteLLM(LITELLM_API_KEY)

    for file_name, prompt in dic.items():
        context = load_file(file_name)
        for model in models:
            the_file = open(
                f"test_{file_name.replace('.json', '')}_{model.replace('/', '_')}_{int(time.time())}.txt",
                "w+",
            )
            the_file.write(f"Prompt: {prompt}\n")
            the_file.write(f"Model: {model}\n")
            try:
                response = litellm_requests.completion_without_proxy(context, model)
                the_file.write(f"Response: {response[1].choices[0].message.content}\n")
            except Exception as ex:
                the_file.write("Response: Failed\n")
                the_file.write(f"Reason: {ex}\n")
            the_file.close()


test()
