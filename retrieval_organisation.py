import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np
from utils import get_embedding_col, generate_embedding


# Connect to PostgreSQL
conn = psycopg2.connect("dbname=postgres user=postgres password=mysecurepassword host=localhost")
cur = conn.cursor()

# Define search query
search_text = "škola"
# search_embedding = model.encode(search_text).tolist()

search_embedding = generate_embedding(search_text)
search_embedding_str = '['+','.join(map(str, search_embedding))+']'

# Perform similarity search (cosine similarity)
cur.execute(f"""
    SELECT id, name, {get_embedding_col()} <=> %s AS similarity
    FROM organisation
    ORDER BY  {get_embedding_col()} <=> %s
    LIMIT 5;
""", (search_embedding_str, search_embedding_str))


# Print results
results = cur.fetchall()
for row in results:
    print(f"ID: {row[0]}, Name: {row[1]}, Similarity: {row[2]}")

# Close connection
cur.close()
conn.close()
