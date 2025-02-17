import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np
from utils import get_embedding_col, generate_embedding
import argparse


# Connect to PostgreSQL
conn = psycopg2.connect("dbname=postgres user=postgres password=mysecurepassword host=localhost")
cur = conn.cursor()

search_text = " pastier ?"

search_embedding = generate_embedding(search_text)
search_embedding_str = '['+','.join(map(str, search_embedding))+']'
print(f"Type of search_embedding: {type(search_embedding)}")

#search_embedding=np.array2string(model.encode(search_text), separator=',')

cur.execute(f"""
    SELECT id, name, {get_embedding_col()} <=> %s AS similarity
    FROM person
    ORDER BY {get_embedding_col()} <=> %s
    LIMIT 2;
""", (search_embedding_str, search_embedding_str))


# Print results
results = cur.fetchall()
for row in results:
    print(f"ID: {row[0]}, Name: {row[1]}, Similarity: {row[2]}")

# Close connection
cur.close()
conn.close()
