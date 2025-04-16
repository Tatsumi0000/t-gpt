import os
from os.path import dirname, join

from dotenv import load_dotenv
from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader


def create_index():
    current_dirname = dirname(__file__)
    dotenv_path = join(current_dirname, "../../.env")
    load_dotenv(dotenv_path)
    print(os.environ["OPENAI_API_KEY"])
    documents = SimpleDirectoryReader(
        input_dir=join(current_dirname, "data")
    ).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist()


if __name__ == "__main__":
    print("Debug")
    create_index()
