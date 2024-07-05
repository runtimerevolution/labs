import os
from dotenv import load_dotenv
from autogen import ConversableAgent, UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor

load_dotenv()
path_for_backend = "/Users/pedroneves/Desktop/AI_TESTS/app.py"
path_for_frontend = "/Users/pedroneves/Desktop/AI_TESTS/templates/index.html"

backend_file = open(path_for_backend, "r")

frontend_file = open(path_for_frontend, "r")

backend = backend_file.read()
frontend = frontend_file.read()

code_executer_context = """
You are an experienced programmer
"""

code_writer_context = """
You are an experienced programmer and the code base you're working is located in this directory /Users/pedroneves/Desktop/AI_TESTS/ you can access it to read and
write all necessary changes you need to complete my requests
"""


llm_config = {"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}
executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir='/Users/pedroneves/Desktop',
)

code_writer = ConversableAgent("code_writer",
                           llm_config=llm_config,
                           code_execution_config=False,
                           system_message=code_writer_context,
                           human_input_mode="ALWAYS",)

code_executer = ConversableAgent("code_executer",
                           llm_config=False,
                           code_execution_config={"executor": executor},
                           system_message=code_executer_context,
                           human_input_mode="NEVER")

# Start the chat
code_executer.initiate_chat(
    code_writer,
    message="""
    Give me some code to read the content of all the files in the directory /Users/pedroneves/Desktop/AI_TESTS including all files inside directories in this one.
    This should be given in a format that you will understand.
    Never use f-string
    Use code in a format that LocalCommandLineCodeExecutor will be able to run
    The output should be separated by the path to each file
    """,
)
