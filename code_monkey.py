from langchain.vectorstores import DeepLake
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models.openai import ChatOpenAI
import openai
from labs.config import OPENAI_API_KEY


session_state_generated = []
session_state_past = []


def run_chat_app(activeloop_dataset_path, user_input="Make a method that prints hello world"):
    global session_state_generated
    global session_state_past

    openai.api_key = OPENAI_API_KEY

    embeddings = OpenAIEmbeddings()

    db = DeepLake(
        dataset_path=activeloop_dataset_path,
        read_only=True,
        embedding_function=embeddings,
    )

    if len(session_state_generated) == 0:
        session_state_generated = ["i am ready to help you sir"]
    if len(session_state_past) == 0:
        session_state_past = ["hello"]

    if user_input:
        output = search_db(db, user_input)
        session_state_past.append(user_input)
        session_state_generated.append(output)

    # If there are generated responses, display the conversation messages.
    if len(session_state_generated) > 0:
        for i in range(len(session_state_generated)):
            print(session_state_past[i])
            print(session_state_generated[i])


def generate_response(prompt):
    """
    Generate a response using OpenAI's ChatCompletion API and the specified prompt.
    """
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    response = completion.choices[0].message.content
    return response


def search_db(db, query):
    """Search for a response to the query in the DeepLake database."""
    # Create a retriever from the DeepLake instance
    retriever = db.as_retriever()
    # Set the search parameters for the retriever
    retriever.search_kwargs["distance_metric"] = "cos"
    retriever.search_kwargs["fetch_k"] = 100
    # retriever.search_kwargs["maximal_marginal_relevance"] = True
    retriever.search_kwargs["k"] = 10
    # Create a ChatOpenAI model instance
    model = ChatOpenAI(model="gpt-3.5-turbo")
    # Create a RetrievalQA instance from the model and retriever
    qa = RetrievalQA.from_llm(model, retriever=retriever)
    # Return the result of the query
    return qa.run(query)


run_chat_app("hub://cmartinez/labs_db")
