from sentence_transformers import SentenceTransformer
import psycopg2
import json
from openai import OpenAI
import sys
from utils import get_embedding_col, generate_embedding

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=postgres user=postgres password=mysecurepassword host=localhost")
cur = conn.cursor()

# Fetch records that need embeddings
cur.execute(f"SELECT id, name, birth_place, death_place, nationality, occupation, spouse, alma_mater, abstract, source, history, description, additional_attributes FROM person WHERE {get_embedding_col()} IS NULL")
records = cur.fetchall()

# Generate and update embeddings
for record in records:
    person_id, name, birth_place, death_place, nationality, occupation, spouse, alma_mater, abstract, source, history, description, additional_attributes = record

    attributes_text = json.dumps(additional_attributes) if additional_attributes else ""
    input_text = f"Name: {name}. Birth Place: {birth_place or ''}. Death Place: {death_place or ''}. Nationality: {nationality or ''}. Occupation: {occupation or ''}. Spouse: {spouse or ''}. Alma Mater: {alma_mater or ''}. Abstract: {abstract or ''}. Source: {source or ''}. History: {history or ''}. Description: {description or ''}. Additional Attributes: {attributes_text}"

    # Generate embedding
    embedding_vector = generate_embedding(input_text)

    # Store embedding back in the database
    cur.execute(f"UPDATE person SET {get_embedding_col()} = %s WHERE id = %s", (embedding_vector, person_id))

# Commit changes
conn.commit()
cur.close()
conn.close()
