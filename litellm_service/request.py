import os
import requests

# from litellm import completion
from langchain.vectorstores import DeepLake
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models.openai import ChatOpenAI
import openai
from labs.config import OPENAI_API_KEY


models = [
    "openai/gpt-3.5-turbo",
    "cohere/command-light",
    "gemini/gemini-pro",
    "groq/llama3-8b-8192",
    "huggingface/tiiuae/falcon-7b-instruct",
]


# class RequestLiteLLM:
#     def __init__(self, litellm_api_key):
#         self.api_key = litellm_api_key

#     def completion(self, messages, model="llm-model"):
#         """
#         messages expected to be in the following format:
#         [
#             {
#                 "role": "user",
#                 "content": ""
#             }
#         ]
#         Where role can be "user", "assistant", "system".
#         And content is the body of the message.
#         """
#         headers = {
#             "Accept": "application/json",
#             "API-Key": self.api_key,
#         }

#         data = {"messages": messages}
#         result = requests.post(
#             f"http://0.0.0.0:4000/chat/completions?model={model}",
#             headers=headers,
#             json=data,
#         )

#         return result.json()

#     def completion_without_proxy(self, messages, model=None):
#         """
#         messages expected to be in the following format:
#         [
#             {
#                 "role": "user",
#                 "content": ""
#             }
#         ]
#         Where role can be "user", "assistant", "system".
#         And content is the body of the message.
#         """
#         if model:
#             return model, completion(
#                 model=model,
#                 messages=messages,
#             )

#         for model in models:
#             try:
#                 response = completion(model=model, messages=messages)
#                 return model, response
#             except Exception as ex:
#                 pass
#         return model, None


class RequestBarebones:
    def __init__(self, activeloop_dataset_path):

        self.embeddings = OpenAIEmbeddings()
        self.db = DeepLake(
            dataset_path=activeloop_dataset_path,
            read_only=True,
            embedding_function=self.embeddings,
        )

    def search_db(self, query):
        retriever = self.db.as_retriever()
        retriever.search_kwargs["distance_metric"] = "cos"
        retriever.search_kwargs["fetch_k"] = 100
        retriever.search_kwargs["k"] = 10

        model = ChatOpenAI(model="gpt-3.5-turbo")
        qa = RetrievalQA.from_llm(model, retriever=retriever)
        return qa.run(query)

    def completion(self, detailed_issue):
        nlp_summary = f"""
        Add a multiplication function to the Calculator class in labs/code_examples/calculator.py and add a unit tests for the new multiplication function in the file labs/code_examples/test_calculator.py file.
        """
        user_input = f"""
        You're a diligent software engineer AI. You can't see, draw, or interact with a browser, but you can read and write files, and you can think.
        You've been given the following task: {detailed_issue}. Your answer will be in yaml format. Please provide a list of actions to perform in order to complete it, considering the current project.
        Each action should contain two fields: action, which is either create or modify; and args, which is a map of key-value pairs, specifying the arguments for that action:
        path - the path of the file to create/modify and content - the content to write to the file.
        Please don't add any text formatting to the answer, making it as clean as possible.
        """
        output = self.search_db(user_input)
        return output
