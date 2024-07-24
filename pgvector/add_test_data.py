from connect import create_db_connection
import psycopg2
from litellm import embedding


if __name__ == "__main__":
    texts = [
        "I like to eat broccoli and bananas.",
        "I ate a banana and spinach smoothie for breakfast.",
        "Chinchillas and kittens are cute.",
        "My sister adopted a kitten yesterday.",
        "Look at this cute hamster munching on a piece of broccoli.",
    ]

    embeddings = embedding(model="text-embedding-ada-002", input=texts)

    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        for text, embedding_obj in zip(texts, embeddings.data):
            cursor.execute(
                "INSERT INTO embeddings (embedding, text) VALUES (%s, %s)",
                (embedding_obj["embedding"], text),
            )
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while writing to DB", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
