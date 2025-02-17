from sentence_transformers import SentenceTransformer
import sys
from openai import OpenAI

client = OpenAI(api_key="")


model_name = sys.argv[1] if len(sys.argv) > 1 else 'default'


def get_embedding_col():

    column_name = f"embedding_{model_name}" if model_name != 'default' else "embedding"
    return  column_name

def generate_embedding(input_text):

    if model_name == 'ada':
        response = client.embeddings.create(input=input_text, model="text-embedding-ada-002")
        return response.data[0].embedding
    else:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        return model.encode(input_text).tolist()
