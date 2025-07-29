import os
import pandas as pd
from groq import Groq
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from dotenv import load_dotenv

env_path_files = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path_files)

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL')
COLLECTION_NAME = os.getenv("FAQ_COLLECTION_NAME", "faq_file")

groq_client = Groq(api_key=GROQ_API_KEY)
chroma_client = chromadb.PersistentClient(path='./chroma_store')


ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='sentence-transformers/all-MiniLM-L6-v2')

def faq_ingestion(path):
    if COLLECTION_NAME not in [c.name for c in chroma_client.list_collections()]:
        collections = chroma_client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=ef #type: ignore
        )
        
        df = pd.read_csv(path)
        docs = df['question'].tolist()
        metadata = [{"answer": ans} for ans in df['answer'].tolist()]
        ids = [f"id_{i}" for i in range(len(docs))]

        collections.add(
            documents=docs,
            metadatas=metadata, #type: ignore
            ids=ids
        )
        print(f"FAQ {COLLECTION_NAME} is ingested sucessfully.")

    else:
        print(f"FAQ {COLLECTION_NAME} exists.")


def generate_prompt_query(query):
    collection = chroma_client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=ef #type: ignore
    )
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    return results

def prompt_query_to_context(query, context):
    prompt = f'''Given the following context and question, generate answer based on this context only.
    If the answer is not found in the context, kindly state "I don't know". Don't try to make up an answer. 
	
    QUESTION: {query}

    CONTEXT: {context}

	'''
    chat_completions = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model=os.environ['GROQ_MODEL'],
        max_completion_tokens=350
    )
    return chat_completions.choices[0].message.content


def chain_prompt_query_to_context(query):
    user_prompt = generate_prompt_query(query)
    context = ' '.join([q.get('answer') for q in user_prompt['metadatas'][0]]) #type: ignore
    llm_ans = prompt_query_to_context(query, context)
    return llm_ans


if __name__ == "__main__":
    file_path = Path(__file__).parent / 'resources' / 'faq_data.csv'
    faq_ingestion(file_path)
    query = 'Do I get discount with the HDFC credit card?'
    final_ans = chain_prompt_query_to_context(query)
    print("Answer:", final_ans)



