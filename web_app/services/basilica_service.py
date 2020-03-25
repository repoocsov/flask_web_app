# web_app/services/basilica_service.py

import basilica
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BASILICA_API_KEY")

def basilica_api_client():
    connection = basilica.Connection(API_KEY)
    return connection

if __name__ == "__main__":
    # Testing client in the CLI
    connection = basilica_api_client()
    sentence = "Hello again"
    sent_embeddings = connection.embed_sentence(sentence)
    sentences = ["Hello world!", "How are you?"]
    embeddings = connection.embed_sentences(sentences)
