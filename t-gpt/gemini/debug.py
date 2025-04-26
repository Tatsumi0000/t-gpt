import os
from os.path import dirname, join

from dotenv import load_dotenv
from llama_index.core import GPTVectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI


def create_index():
    current_dirname = dirname(__file__)
    dotenv_path = join(current_dirname, "../../.env")
    load_dotenv(dotenv_path)
    Settings.llm = GoogleGenAI(model_name="models/gemini-1.5-flash")
    Settings.embed_model = GoogleGenAIEmbedding(model_name="models/embedding-001")
    documents = SimpleDirectoryReader(join(current_dirname, "data")).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    print(
        query_engine.query(
            "ジャンプ流!DVD付分冊マンガ講座(8) 2016年 5/2 号では何が見れますか？"
        )
    )


if __name__ == "__main__":
    print("start!!!")
    create_index()
